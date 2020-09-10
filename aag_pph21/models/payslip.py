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
    
    tunj_pph = fields.Float("Tunjangan PPH")
    pot_pph = fields.Float("Pot PPH")

    def compute_sheet(self):
        res = super(payslip, self).compute_sheet() 
        _logger.info("--- compute sheet --- %s", self.line_ids )
        self._calculate_pph()

        i=0
        while self.pot_pph - self.tunj_pph != 0:
            _logger.info("--- iterasi %s", i)
            self.tunj_pph = self.pot_pph
            self._calculate_pph()
            i+=1
        return res 

    def _calculate_pph(self):
        _logger.info("--- awal bruto = %s", self.bruto)
        _logger.info("--- new tunj_pph = %s", self.tunj_pph)
        self.bruto = (self.contract_id.wage + self.contract_id.x_trans + self.contract_id.x_occup + self.contract_id.x_family + self.contract_id.x_functional + self.contract_id.x_perform + self.tunj_pph)*12
        _logger.info("--- new bruto = %s", self.bruto)
        self.env.cr.commit()

        self.bjab = min(0.05 * self.bruto , 6000000)	
        self.netto = self.bruto-self.bjab-(self.contract_id.wage + self.contract_id.x_tpk + self.contract_id.x_occup + self.contract_id.x_trans + self.contract_id.x_family + self.contract_id.x_presence + self.contract_id.x_functional)*0.02*12			
        self.pkp = self.netto - self.ptkp if self.netto - self.ptkp >0 else 0
        self.pph21_thn = self.get_pph21_setahun()
        self.pot_pph = self.pph21_thn/12

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

