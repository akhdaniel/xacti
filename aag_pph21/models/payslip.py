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
       
    tunj_pph = fields.Integer("Tunjangan PPH")
    pot_pph = fields.Integer("Pot PPH")
    pph21med = fields.Integer("PPh21 Medical")
    
    
    def compute_sheet(self):
        res = super(payslip, self).compute_sheet() 
        _logger.info("--- compute sheet --- %s", self.line_ids )


        # cari selisih med_reimburse
        # cari selisih overtime
        # cari selisih TRH
        # cari selisih bonus 
        
        # dengan med_reimburse
        self._calculate_pph(med_reimburse=True)
        i=0
        selisih = round(self.pot_pph - self.tunj_pph)
        while selisih != 0:
            _logger.info("--- iterasi %s, selisih1=%s", i, selisih)
            self.tunj_pph = self.pot_pph
            self._calculate_pph(med_reimburse=True)
            selisih = round(self.pot_pph - self.tunj_pph)
            i+=1

        self.pph21med = self.pot_pph          

        # tanpa med_reimburse
        self._calculate_pph(med_reimburse=False)
        i=0
        selisih = round(self.pot_pph - self.tunj_pph)
        while selisih != 0:
            _logger.info("--- iterasi %s, selisih1=%s", i, selisih)
            self.tunj_pph = self.pot_pph
            self._calculate_pph(med_reimburse=False)
            selisih = round(self.pot_pph - self.tunj_pph)
            i+=1

        self.pph21med = self.pph21med  - self.pot_pph


        return res 

    def _calculate_pph(self, med_reimburse = False):
        _logger.info("--- awal bruto = %s", self.bruto)
        _logger.info("--- new tunj_pph = %s", self.tunj_pph)
    
        INPUT_MED_REIMBURSE=0
        for inp in self.input_line_ids: 
            if inp.code=='INPUT_MED_REIMBURSE' and med_reimburse:
                INPUT_MED_REIMBURSE=inp.amount

        TJHTCOM=0
        TACCTCOM=0
        TDTHCOM=0
        JHTEMP=0
        PENEMP=0
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
            
        self.bruto = (self.contract_id.wage + self.contract_id.x_trans + self.contract_id.x_occup + self.contract_id.x_family + self.contract_id.x_functional + self.contract_id.x_perform + self.tunj_pph + INPUT_MED_REIMBURSE + TJHTCOM + TACCCOM + TDTHCOM)*12
        _logger.info("--- new bruto = %s", self.bruto)
        self.env.cr.commit()

        self.bjab = min(0.05 * self.bruto , 6000000)	
        self.netto = self.bruto-self.bjab-(JHTEMP + PENEMP) * 12			
        self.pkp = self.netto - self.ptkp if self.netto - self.ptkp >0 else 0
        self.pph21_thn = round(self.get_pph21_setahun(), 0)
        self.pot_pph = round(self.pph21_thn/12, 0)

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

