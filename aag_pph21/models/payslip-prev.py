from odoo import models, fields, api, _
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)



class payslip(models.Model):
    _inherit = 'hr.payslip'
    ptkp = fields.Integer("PTKP", related="employee_id.ptkp_id.nominal")
    bruto = fields.Integer("Bruto", )
    bjab = fields.Integer("Biaya Jabatan", )
    netto = fields.Integer("Netto", )
    pkp = fields.Integer("PKP", )
    pph21_thn = fields.Integer("PPH21 Setahun", )
    pph21_paid = fields.Integer("PPh21 Paid")
      
    tunj_pph = fields.Integer("Tunjangan PPH")
    pot_pph = fields.Integer("Pot PPH")

    pph21med = fields.Integer("PPh21 Medical")
    pph21ovt = fields.Integer("PPh21 Overtime")
    pph21thr = fields.Integer("PPh21 THR")
    pph21bon = fields.Integer("PPh21 Bonus")
    pph21irr = fields.Integer("PPh21 Irregular")
    pph21reg = fields.Integer("PPh21 Regular")
    
    def compute_sheet(self):
        res = super(payslip, self).compute_sheet() 
        _logger.info("--- compute sheet --- %s", self.line_ids )


        # dengan medical, overtime
        self._calculate_pph(medical=True, overtime=True, thr=True, bonus=True)
        i=0
        selisih = round(self.pot_pph - self.tunj_pph)
        while selisih != 0:
            _logger.info("--- iterasi %s, selisih1=%s", i, selisih)
            self.tunj_pph = self.pot_pph
            self._calculate_pph(medical=True, overtime=True, thr=True, bonus=True) 
            selisih = round(self.pot_pph - self.tunj_pph)
            i+=1

        pph_all = self.pot_pph 

        # cari selisih medical
        self.cari_selisih('pph21med', pph_all)

        # cari selisih overtime
        self.cari_selisih('pph21ovt', pph_all)

        # cari selisih THR
        self.cari_selisih('pph21thr', pph_all)

        # cari selisih bonus 
        self.cari_selisih('pph21bon', pph_all)
        
        self.pot_pph = pph_all
        self.tunj_pph = pph_all
        self.pph21irr = self.pph21ovt + self.pph21med + self.pph21thr + self.pph21bon
        self.pph21reg = pph_all - self.pph21irr
                
        return res 

    def cari_selisih(self, komponen, pph_all):

        if komponen == 'pph21med':
            medical = False
            overtime = True
            thr = True
            bonus = True
        elif komponen == 'pph21ovt':
            medical = True
            overtime = False
            thr = True
            bonus = True
        elif komponen == 'pph21thr':
            medical = True
            overtime = True
            thr = False
            bonus = True
        elif komponen == 'pph21bon':
            medical = True
            overtime = True
            thr = True
            bonus = False


        # tanpa medical, overtime
        
        self._calculate_pph(medical=medical, overtime=overtime, thr=thr, bonus=bonus)
        
        i=0
        selisih = round(self.pot_pph - self.tunj_pph)
        while selisih != 0:
            _logger.info("--- iterasi %s, selisih1=%s", i, selisih)
            self.tunj_pph = self.pot_pph
            self._calculate_pph(medical=medical, overtime=overtime, thr=thr, bonus=bonus)
            selisih = round(self.pot_pph - self.tunj_pph)
            i+=1
        # self.pph21med = self.pph21med  - self.pot_pph
        setattr(self, komponen, pph_all - self.pot_pph)


    def _calculate_pph(self, medical=True, overtime=True, thr=True, bonus=True ):
        _logger.info("--- awal bruto = %s", self.bruto)
        _logger.info("--- new tunj_pph = %s", self.tunj_pph)
    
        INPUT_MEDICAL=0
        INPUT_OVERTIME=0
        INPUT_THR=0
        INPUT_BONUS=0

        for inp in self.input_line_ids: 
            if inp.code=='INPUT_MEDICAL' and medical:
                INPUT_MEDICAL=inp.amount

            if inp.code=='INPUT_OVERTIME' and overtime:
                INPUT_OVERTIME=inp.amount
            
            if inp.code=='INPUT_THR' and thr:
                INPUT_THR=inp.amount

            if inp.code=='INPUT_BONUS' and bonus:
                INPUT_BONUS=inp.amount

        TJHTCOM=0
        TACCCOM=0
        TDTHCOM=0
        JHTEMP=0
        PENEMP=0
        TBPJSKES_DTP=0

        for line in self.line_ids: 
            if line.code=='TJHTCOM':
                TJHTCOM=line.amount
            if line.code=='TACCCOM':
                TACCCOM=line.amount
            if line.code=='TDTHCOM':
                TDTHCOM=line.amount
            if line.code=='JHTEMP':
                JHTEMP=line.amount
            if line.code=='PENEMP':
                PENEMP=line.amount
            if line.code=='BPJSKES':
                TBPJSKES_DTP=line.amount
        
        akumulasi = self.cari_akumulasi(medical=medical, overtime=overtime, thr=thr, bonus=bonus )
        
        curr_reg_income = self.contract_id.wage + self.contract_id.x_trans + self.contract_id.x_occup + self.contract_id.x_family + self.contract_id.x_functional + self.contract_id.x_perform + self.tunj_pph + TJHTCOM + TACCCOM + TDTHCOM + TBPJSKES_DTP

        total_reg_income_accum = curr_reg_income + (akumulasi['x_accgrs'] if akumulasi else 0)

        curr_irr_income = INPUT_MEDICAL + INPUT_THR + INPUT_BONUS

        total_irr_income_accum =  curr_irr_income + (akumulasi['x_accovt']+akumulasi['x_accmed']+akumulasi['x_accthr']+akumulasi['x_accbon'] if akumulasi else 0)

        curr_empl_pension = JHTEMP + PENEMP

        total_empl_pension_accum =  curr_empl_pension + (akumulasi['x_accjht2']+akumulasi['x_accpen1'] if akumulasi else 0)
        
        # self.bruto = (curr_reg_income * 12) + curr_irr_income 
        # ganti kalkulasi menjadi: 
        bulan_berjalan = self.date_to.month 
        self.bruto = ( total_reg_income_accum * 12 )/bulan_berjalan + total_irr_income_accum

        _logger.info("--- new bruto = %s", self.bruto)
        self.env.cr.commit()

        self.bjab = min(0.05 * self.bruto , 6000000)	
        # self.netto = self.bruto-self.bjab-((total_empl_pension_accum * 12)/bulan_berjalan)
        self.netto = self.bruto-self.bjab-total_empl_pension_accum 			
        self.pkp = self.netto - self.ptkp if self.netto - self.ptkp >0 else 0
        self.pph21_thn = round(self.get_pph21_setahun(), 0)
        pph_sdh_dibayar = akumulasi['x_pph_accgrs']+akumulasi['x_pph_accovt']+akumulasi['x_pph_accmed']+akumulasi['x_pph_accthr']+akumulasi['x_pph_accbon'] if akumulasi else 0
        self.pph21_paid = pph_sdh_dibayar
        self.pot_pph = round(self.pph21_thn/12 * bulan_berjalan - pph_sdh_dibayar, 0)
        # bisa minus, kalau minus -> pot_pph=0.. min(pot_pph, 0 )
        # self.pot_pph = max(self.pot_pph, 0)
    
    def get_pph21_setahun(self):
        sisa_pkp = self.pkp 
        pph21 = 0 
        range = self.contract_id.company_id.pkp_ids[0]
        if self.pkp > range.maximum:
            pph21 += range.maximum * range.rate / 100 
            sisa_pkp = self.pkp - range.maximum
            range = self.contract_id.company_id.pkp_ids[1]
            if sisa_pkp <= (range.maximum-range.minimum+1):
                pph21 += sisa_pkp*range.rate/100 
            else:
                pph21 += (range.maximum-range.minimum+1) * range.rate / 100
                sisa_pkp = sisa_pkp-(range.maximum-range.minimum+1)
                range = self.contract_id.company_id.pkp_ids[2]
                if sisa_pkp <= (range.maximum-range.minimum+1):
                    pph21 += sisa_pkp*range.rate/100
                else:
                    pph21 += (range.maximum-range.minimum+1)*range.rate/100
                    sisa_pkp = sisa_pkp-(range.maximum-range.minimum+1)
                    range = self.contract_id.company_id.pkp_ids[3]
                    pph21 += sisa_pkp*range.rate/100
        else:
            pph21 = self.pkp*range.rate/100        
        return pph21

    def cari_akumulasi(self, medical=True, overtime=True, thr=True, bonus=True):
        cr = self.env.cr
        sql = "select * from aag_pph_accumulation_aag_pph_accumulation where idno=%s"
        cr.execute(sql, (self.employee_id.x_idno,))
        akumulasi = cr.dictfetchone()

        if not medical:
            akumulasi['x_accmed'] = 0

        if not overtime:
            akumulasi['x_accovt'] = 0

        if not thr:
            akumulasi['x_accthr'] = 0

        if not bonus:
            akumulasi['x_accbon'] = 0

        return akumulasi
