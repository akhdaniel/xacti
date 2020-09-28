#from odoo import models, fields, api, _
#from odoo.exceptions import UserError

#import logging
#_logger = logging.getLogger(__name__)

#=============
from datetime import date, datetime, time, timedelta

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, tools, _, SUPERUSER_ID
import pdb
import dateutil.parser
from pytz import timezone

import logging
_logger = logging.getLogger(__name__)



class payslip(models.Model):
    _inherit = 'hr.payslip'
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

    @api.model
    def get_inputs(self, contracts, date_from, date_to):
        res = super(payslip, self).get_inputs(contracts, date_from, date_to) 

        # dengan medical, overtime
        self._calculate_pph(contracts, medical=True, overtime=True, thr=True, bonus=True)
        i=0
        selisih = round(self.pot_pph - self.tunj_pph)
        while selisih != 0:
            _logger.info("--- iterasi %s, selisih1=%s", i, selisih)
            self.tunj_pph = self.pot_pph
            self._calculate_pph(contracts, medical=True, overtime=True, thr=True, bonus=True) 
            selisih = round(self.pot_pph - self.tunj_pph)
            i+=1

        pph_all = self.pot_pph 

        # cari selisih medical
        self._cari_selisih(contracts, 'pph21med', pph_all)
    
        # cari selisih overtime
        self._cari_selisih(contracts, 'pph21ovt', pph_all)
    
        # cari selisih THR
        self._cari_selisih(contracts, 'pph21thr', pph_all)
    
        # cari selisih bonus 
        self._cari_selisih(contracts, 'pph21bon', pph_all)
    
        irr_acc = self._find_irr_acc(contracts)        
        self.pph21ovt = self.pph21ovt - (irr_acc['x_pph_accovt'] if irr_acc else 0)
        self.pph21med = self.pph21med - (irr_acc['x_pph_accmed'] if irr_acc else 0)
        self.pph21thr = self.pph21thr - (irr_acc['x_pph_accthr'] if irr_acc else 0)
        self.pph21bon = self.pph21bon - (irr_acc['x_pph_accbon'] if irr_acc else 0)

        self.pot_pph = pph_all - (irr_acc['x_pph_accgrs']+irr_acc['x_pph_accovt']+irr_acc['x_pph_accmed']+irr_acc['x_pph_accthr']+irr_acc['x_pph_accbon'] if irr_acc else 0)
        self.tunj_pph = pph_all - (irr_acc['x_pph_accgrs']+irr_acc['x_pph_accovt']+irr_acc['x_pph_accmed']+irr_acc['x_pph_accthr']+irr_acc['x_pph_accbon'] if irr_acc else 0)

        self.pph21irr = self.pph21ovt + self.pph21med + self.pph21thr + self.pph21bon
        self.pph21reg = self.pot_pph - self.pph21irr
                
        return res 

    def _cari_selisih(self, contracts, komponen, pph_all):

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
        
        self._calculate_pph(contracts, medical=medical, overtime=overtime, thr=thr, bonus=bonus)
        
        i=0
        selisih = round(self.pot_pph - self.tunj_pph)
        while selisih != 0:
            _logger.info("--- iterasi %s, selisih1=%s", i, selisih)
            self.tunj_pph = self.pot_pph
            self._calculate_pph(contracts, medical=medical, overtime=overtime, thr=thr, bonus=bonus)
            selisih = round(self.pot_pph - self.tunj_pph)
            i+=1
        # self.pph21med = self.pph21med  - self.pot_pph
        setattr(self, komponen, pph_all - self.pot_pph)


    def _calculate_pph(self, contracts, medical=True, overtime=True, thr=True, bonus=True ):
    #    _logger.info("--- awal bruto = %s", self.bruto)
        _logger.info("--- awal bruto = %s", self.bruto)
    
    #    _logger.info("--- new tunj_pph = %s", self.tunj_pph)
        _logger.info("--- new tunj_pph = %s", self.tunj_pph)


# ==== GET DATA FROM PAYSLIP TO FIND CUURENT MONTH ACTUAL INCOME/DEDUCTION ==== 
 # ==== INIT. INCOME RULE'S CODE ==== 
    # == REGULAR INCOME
        BASIC=0
        I_BASIC=0
        I_TPK=0
        I_OCCUP=0
        I_PRESENCE=0
        I_FAMILY=0
        I_FUNCTIONAL=0
        I_TRANSPORT=0
        I_PERFORM=0
        I_OTHER=0
        I_SHIFT=0
        # I_MEAL=0        UANG MAKAN TDK DIPUNGUT PAJAK
        I_JHTCOM=0
        I_ACCCOM=0
        I_DTHCOM=0
        I_BPJSKES_COM=0
    # == IRREGULAR INCOME ==
        I_OVERTIME=0
        I_MEDICAL=0
        I_THR=0
        I_BONUS=0

 # ==== INIT. DEDUCTION RULE'S CODE ==== 
    # == REGULAR INCOME
        D_BASIC=0
    #    D_TPK=0
    #    D_OCCUP=0
    #    D_PRESENCE=0
    #    D_FAMILY=0
    #    D_FUNCTIONAL=0
        D_TRANSPORT=0
    #    D_PERFORM=0
        D_OTHER=0
    #    D_SHIFT=0
    #    D_MEAL=0
    #    D_JHTCOM=0
    #    D_ACCCOM=0
    #    D_DTHCOM=0
    #    D_BPJSKES_COM=0

        D_JHTEMP=0
        D_PENEMP=0
    #   D_BPJSKES_EMP=0

    # == IRREGULAR INCOME ==
    #    D_OVERTIME=0
    #    D_MEDIC=0
    #    D_THR=0
    #    D_BONUS=0

# ==== READ DATA FROM PAYSLIP ==== 
    # === READ INCOME ====
        for line in self.line_ids: 
            if line.code=='BASIC':
                BASIC=line.amount
            if line.code=='I_BASIC':
                I_BASIC=line.amount
            if line.code=='I_TPK':
                I_TPK=line.amount
            if line.code=='I_OCCUP':
                I_OCCUP=line.amount
            if line.code=='I_PRESENCE':
                I_PRESENCE=line.amount
            if line.code=='I_FAMILY':
                I_FAMILY=line.amount
            if line.code=='I_FUNCTIONAL':
                I_FUNCTIONAL=line.amount
            if line.code=='I_TRANSPORT':
                I_TRANSPORT=line.amount
            if line.code=='I_PERFORM':
                I_PERFORM=line.amount
            if line.code=='I_OTHER':
                I_OTHER=line.amount
            if line.code=='I_SHIFT':
                I_SHIFT=line.amount
#            if line.code=='I_MEAL':
#                I_MEAL=line.amount
            if line.code=='I_JHTCOM':
                I_JHTCOM=line.amount
            if line.code=='I_ACCCOM':
                I_ACCCOM=line.amount
            if line.code=='I_DTHCOM':
                I_DTHCOM=line.amount
            if line.code=='I_BPJSKES_COM':
                I_BPJSKES_COM=line.amount

            if line.code=='I_OVERTIME':
                I_OVERTIME=line.amount
            if line.code=='I_MEDICAL':
                I_MEDICAL=line.amount
            if line.code=='I_THR':
                I_THR=line.amount
            if line.code=='I_BONUS':
                I_BONUS=line.amount
    # === READ DEDUCTION ====
            if line.code=='D_BASIC':
                D_BASIC=line.amount
            if line.code=='D_TRANSPORT':
                D_TRANSPORT=line.amount
            if line.code=='D_OTHER':
                D_OTHER=line.amount

            if line.code=='D_JHTEMP':
                D_JHTEMP=line.amount
            if line.code=='D_PENEMP':
                D_PENEMP=line.amount
#            if line.code=='D_BPJSKES_EMP':
#                D_BPJSKES_EMP=line.amount

# === CALCULATE NET INCOME =======================
        net_basic=BASIC+I_BASIC-D_BASIC
        # I_TPK=I_TPK-D_TPK
        # I_OCCUP=I_OCCUP-D_OCCUP
        # I_PRESENCE=I_PRESENCE-D_PRESENCE
        # I_FAMILY=I_FAMILY-D_FAMILY
        # I_FUNCTIONAL=I_FUNCTIONAL-D_FUNCTIONAL
        net_transport=I_TRANSPORT-D_TRANSPORT
        # I_PERFORM=I_PERFORM-D_PERFORM
        net_other=I_OTHER-D_OTHER
        # I_SHIFT=I_SHIFT-D_SHIFT
        # I_MEAL=I_MEAL-D_MEAL
        # I_JHTCOM=0
        # I_ACCCOM=0
        # I_DTHCOM=0
        # I_BPJSKES_COM=0
    # == IRREGULAR INCOME ==
        # I_OVERTIME=0
        # I_MEDICAL=0
        # I_THR=0
        # I_BONUS=0


        akumulasi = self.cari_akumulasi(contracts, medical=medical, overtime=overtime, thr=thr, bonus=bonus )
        
        # curr_reg_income = self.contract_id.wage + self.contract_id.x_trans + self.contract_id.x_occup + self.contract_id.x_family + self.contract_id.x_functional + self.contract_id.x_perform + self.tunj_pph + TJHTCOM + TACCCOM + TDTHCOM + TBPJSKES_DTP
        curr_reg_income = net_basic+I_TPK+net_transport+I_PRESENCE+I_OCCUP+I_FAMILY+I_FUNCTIONAL+I_PERFORM+net_other+I_SHIFT+self.tunj_pph+I_JHTCOM+I_ACCCOM+I_DTHCOM+I_BPJSKES_COM

        total_reg_income_accum = curr_reg_income + (akumulasi['x_accgrs'] if akumulasi else 0)

        curr_irr_income = I_OVERTIME + I_MEDICAL + I_THR + I_BONUS

        total_irr_income_accum =  curr_irr_income + (akumulasi['x_accovt']+akumulasi['x_accmed']+akumulasi['x_accthr']+akumulasi['x_accbon'] if akumulasi else 0)

        curr_empl_pension = D_JHTEMP + D_PENEMP

        total_empl_pension_accum =  curr_empl_pension + (akumulasi['x_accjht2']+akumulasi['x_accpen1'] if akumulasi else 0)
        
        # self.bruto = (curr_reg_income * 12) + curr_irr_income 
        # ganti kalkulasi menjadi: 
        bulan_berjalan = self.date_to.month 
        self.bruto = ( total_reg_income_accum * 12 )/bulan_berjalan + total_irr_income_accum

        _logger.info("--- new bruto = %s", self.bruto)
        self.env.cr.commit()

        self.bjab = min(0.05 * self.bruto , 6000000)	
        self.netto = self.bruto-self.bjab-((total_empl_pension_accum * 12)/bulan_berjalan)
        # self.netto = self.bruto-self.bjab-total_empl_pension_accum 			
        self.pkp = self.netto - self.ptkp if self.netto - self.ptkp >0 else 0
        self.pph21_thn = round(self.get_pph21_setahun(contracts), 0)
        pph_sdh_dibayar = akumulasi['x_pph_accgrs']+akumulasi['x_pph_accovt']+akumulasi['x_pph_accmed']+akumulasi['x_pph_accthr']+akumulasi['x_pph_accbon'] if akumulasi else 0
        self.pph21_paid = pph_sdh_dibayar

        # untuk selisih irrregular income
        # pengurangan sudah dibayar (pph_sdh_dibayar) dihitung saat sudah didapat selisihnya
        # self.pot_pph = round(self.pph21_thn/12 * bulan_berjalan - pph_sdh_dibayar, 0)
        
        self.pot_pph = round(self.pph21_thn/12 * bulan_berjalan, 0)
        # bisa minus, kalau minus -> pot_pph=0.. min(pot_pph, 0 )
        # self.pot_pph = max(self.pot_pph, 0)
    
    def get_pph21_setahun(self, contracts):
        sisa_pkp = self.pkp 
        pph21 = 0 
        range = contracts.company_id.pkp_ids[0]
        if self.pkp > range.maximum:
            pph21 += range.maximum * range.rate / 100 
            sisa_pkp = self.pkp - range.maximum
            range = contracts.company_id.pkp_ids[1]
            if sisa_pkp <= (range.maximum-range.minimum+1):
                pph21 += sisa_pkp*range.rate/100 
            else:
                pph21 += (range.maximum-range.minimum+1) * range.rate / 100
                sisa_pkp = sisa_pkp-(range.maximum-range.minimum+1)
                range = contracts.company_id.pkp_ids[2]
                if sisa_pkp <= (range.maximum-range.minimum+1):
                    pph21 += sisa_pkp*range.rate/100
                else:
                    pph21 += (range.maximum-range.minimum+1)*range.rate/100
                    sisa_pkp = sisa_pkp-(range.maximum-range.minimum+1)
                    range = contracts.company_id.pkp_ids[3]
                    pph21 += sisa_pkp*range.rate/100
        else:
            pph21 = self.pkp*range.rate/100        
        return pph21

    # def cari_akumulasi(self, medical=True, overtime=True, thr=True, bonus=True):
    def cari_akumulasi(self, contracts, medical=True, overtime=True, thr=True, bonus=True):
    
        cr = self.env.cr
        sql = "select * from aag_pph_accumulation_aag_pph_accumulation where idno=%s"
        # cr.execute(sql, (self.employee_id.x_idno,))
        cr.execute(sql, (contracts.employee_id.x_idno,))

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

    def _find_irr_acc(self, contracts):
        cr = self.env.cr
        sql = "select * from aag_pph_accumulation_aag_pph_accumulation where idno=%s"
        cr.execute(sql, (contracts.employee_id.x_idno,))
        irr_acc = cr.dictfetchone()

        return irr_acc    
