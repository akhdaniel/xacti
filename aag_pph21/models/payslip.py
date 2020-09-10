from odoo import models, fields, api, _
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)



class payslip(models.Model):
    _inherit = 'hr.payslip'

    ptkp = fields.Integer("PTKP", related="employee_id.ptkp_id.nominal")
    bruto = fields.Integer("Bruto", compute="_get_pph")
    bjab = fields.Integer("Biaya Jabatan", compute="_get_pph")
    netto = fields.Integer("Netto", compute="_get_pph")
    pkp = fields.Integer("PKP", compute="_get_pph")
    pph21_thn = fields.Integer("PPH21 Setahun", compute="_get_pph")
    
    tunj_pph = fields.Float("Tunjangan PPH")
    pot_pph = fields.Float("Pot PPH")

    def compute_sheet(self):
        res = super(payslip, self).compute_sheet() 
        _logger.info("--- compute sheet --- %s", self.line_ids )
        self.iterate_pph()
        return res 

    def _get_pph(self):
        for rec in self:
            rec.bruto = (rec.contract_id.wage + rec.contract_id.x_trans + rec.contract_id.x_occup + rec.contract_id.x_family + rec.contract_id.x_functional + rec.contract_id.x_perform)*12
            rec.bjab = min(0.05 * rec.bruto , 6000000)	
            rec.netto = rec.bruto-rec.bjab-(rec.contract_id.wage + rec.contract_id.x_tpk + rec.contract_id.x_occup + rec.contract_id.x_trans + rec.contract_id.x_family + rec.contract_id.x_presence + rec.contract_id.x_functional)*0.02*12			
            rec.pkp = rec.netto - rec.ptkp if rec.netto - rec.ptkp >0 else 0
            rec.pph21_thn = self.get_pph21_setahun(rec)

    def get_pph21_setahun(self, rec):
        sisa_pkp = rec.pkp 
        pph21 = 0 
        range = rec.contract_id.company_id.pkp_ids[0]
        if rec.pkp > range.maximum:
            pph21 += range.maximum * range.rate / 100 
            sisa_pkp = rec.pkp - range.maximum
            range = rec.contract_id.company_id.pkp_ids[1]
            if sisa_pkp <= (range.maximum-range.minimum+1):
                pph21 += sisa_pkp*range.rate/100 
            else:
                pph21 += (range.maximum-range.minimum+1) * range.rate / 100
                sisa_pkp = sisa_pkp-(range.maximum-range.minimum+1)
                range = rec.contract_id.company_id.pkp_ids[2]
                if sisa_pkp <= (range.maximum-range.minimum+1):
                    pph21 += sisa_pkp*range.rate/100
                else:
                    pph21 += (range.maximum-range.minimum+1)*range.rate/100
                    sisa_pkp = sisa_pkp-(range.maximum-range.minimum+1)
                    range = rec.contract_id.company_id.pkp_ids[3]
                    pph21 += sisa_pkp*range.rate/100
        else:
            pph21 = rec.pkp*range.rate/100        
        return pph21

    def iterate_pph(self):
        for  