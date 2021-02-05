# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
import odoo.tools
import time
_logger = logging.getLogger(__name__)
import xlsxwriter

import base64
from io import BytesIO
# from io import StringIO

class report_header(models.Model):
    _name = 'aag.pph21_header'
    _description = 'PPh21 Tahunan'

    name = fields.Char("Name")
    month = fields.Integer("Month")
    year = fields.Integer("Year")

    export_file = fields.Binary("Export File")
    export_filename = fields.Char(string="Export File Name",  )

    detail_ids = fields.One2many(comodel_name="aag.pph21_detail", inverse_name="header_id")
    tmp_dir = '/tmp/'

    def init(self):
        _logger.info("creating aag_hitung_pph")
        self.env.cr.execute("""CREATE OR REPLACE FUNCTION public.aag_hitung_pph(
                v_header_id integer, v_company_id integer)
                RETURNS void
                LANGUAGE 'plpgsql'

                COST 100
                VOLATILE 

            AS $BODY$
            DECLARE
                v_detail record;
                v_sisa_pkp numeric;
                v_pph21 numeric;
                v_pph21x numeric;
                v_range record;
                v_bruto numeric;
                v_tunj_pph numeric;
                v_selisih numeric;
                v_counter numeric;
                v_b02tpp numeric;
                v_sequences integer;

            BEGIN
                delete from aag_pph21_detail where header_id = v_header_id;
                INSERT INTO aag_pph21_detail (
                    header_id,
                    "idno",
                    "aimspj", "aithpj", "aipemb", "ainobp", "aimsp1",
                    "aimsp2", "ainppg", "ainipg", "ainama", "aialam",
                    "aijkel", "aisptk", "aitang", "aijbpg", "aiwpln",
                    "aikneg",
                    "bkdpjk",
                    "b01gji", "b02tpp", "b03tll", "b04hnr", "b05pre",
                    "b06nat", "b07bns", "b08bru", "b09jab", "b10tht",
                    "b11jpe", "b12net", "b13nes", "b14npp", "b15ptk",
                    "b16pkp", "b17pph", "b18pps", "b19hut", "b20lns",
                    "cispin", "cinpwp", "cinama", "citgbp"
                ) 
                SELECT 
                    v_header_id,
                    emp.x_idno,
                    ytd.m_curmm,y_year,0,'1.1-12.20-0000001',ytd.y_strmm,
                    ytd.y_endmm, emp.x_npwp, emp.identification_id, upper(emp.name), 'DEPOK', 
                    case when emp.gender='male' then 'M' else 'F' end as aijkel,
                    case 
                        when ptkp.name='TK/0' or ptkp.name='TK/1' or ptkp.name='TK/2' or ptkp.name='TK/3' then 'TK'
                        when ptkp.name='K/0' or ptkp.name='K/1' or ptkp.name='K/2' or ptkp.name='K/3' then 'K'
                        else 'TK'
                    end as aisptk,
                    case 
                        when ptkp.name='TK/1' or ptkp.name='K/1' then 1
                        when ptkp.name='TK/2' or ptkp.name='K/2' then 2
                        when ptkp.name='TK/3' or ptkp.name='K/3' then 3
                        else 0
                    end as aitang,

                    'Staff','N',
                    '',
                    '21-100-01',
                    y_basic + y_tpk + y_occup + y_functional + y_family + y_perform + y_transport + y_presence + y_other + y_meal + y_shift + y_leave + y_medical,
                    0, y_overtime, 0, y_acccom + y_dthcom + y_bpjs_com,
                    0, y_bonus + y_thr, 0, 0, y_jhtemp + y_penemp,
                    0, 0, 0, 0, ptkp.nominal,
                    0, 0, 0, 0, 0,
                    '', '580178119061000', 'YOSHIKIYO MORIKAWA', '31/01/2021'
                from 
                    aag_salary_ytd_aag_salary_ytd ytd 
                join 
                    hr_employee emp on ytd.idno = emp.x_idno
                join 
                    aag_master_ptkp ptkp on ptkp.id = emp.ptkp_id;

                -- Hitung PPh21 dari PKP 
                v_sequences = 1;
                for v_detail in select * from aag_pph21_detail where header_id=v_header_id
                loop
                    v_pph21 = aag_hitung_pot_pph(v_detail.id,0);
                    v_b02tpp = v_pph21;
                    v_selisih = v_pph21;

                    while round(v_selisih) <> 0
                    loop 
                        v_b02tpp = v_pph21;
						v_pph21 = aag_hitung_pot_pph(v_detail.id,v_b02tpp);
                        v_selisih =  v_pph21 - v_b02tpp;
                        -- raise notice '% %', v_selisih, v_b02tpp;  
                    end loop;
                    update aag_pph21_detail set ainobp = '1-1-12-'|| substring(v_detail.aithpj::text,3,2) || '-' || LPAD(v_sequences::text, 7, '0') where id=v_detail.id;
                    v_sequences = v_sequences + 1;
                end loop;

            END;
            $BODY$;

        """)

        self.env.cr.execute("""CREATE OR REPLACE FUNCTION public.aag_hitung_pot_pph(
                v_detail_id integer, v_b02tpp numeric)
                RETURNS numeric
                LANGUAGE 'plpgsql'

                COST 100
                VOLATILE 

            AS $BODY$
            DECLARE
				v_detail record;
                v_b08bru numeric;
                v_b09jab numeric;
                v_b11jpe numeric;
                v_b12net numeric;
                v_b14npp numeric;
                v_b16pkp numeric;

                v_sisa_pkp numeric;
                v_pph21 numeric;
                v_pph21x numeric;
                v_range record;
                v_bruto numeric;
                v_tunj_pph numeric;
                v_selisih numeric;
                v_counter numeric;

            BEGIN
				select * from aag_pph21_detail where id=v_detail_id into v_detail;
                v_b08bru = v_detail.b01gji + v_b02tpp + v_detail.b03tll + v_detail.b04hnr + v_detail.b05pre + v_detail.b06nat + v_detail.b07bns;  -- bruto tanpa tunjangan pph.
                v_b09jab = LEAST(v_b08bru * 0.05, 6000000);
                v_b11jpe = v_b09jab + v_detail.b10tht;
                v_b12net = v_b08bru - v_b11jpe;
                v_b14npp = v_b12net - v_detail.b13nes;
                if v_detail.aimspj <> 12 then 
                    v_b14npp = (v_b14npp/v_detail.aimspj) * 12;
                end if;
                v_b16pkp = GREATEST(floor((v_b14npp - v_detail.b15ptk)/1000) * 1000,0);                    
                v_sisa_pkp=v_b16pkp;
                v_pph21=0;

                select * from aag_master_pkp limit 1 offset 0 into v_range;
                if v_b16pkp <= v_range.maximum then
                    v_pph21 = v_b16pkp * v_range.rate / 100;
                else
                    v_pph21 = v_pph21 + v_range.maximum * v_range.rate / 100;
                    v_sisa_pkp = v_b16pkp - v_range.maximum;
                    select * from aag_master_pkp limit 1 offset 1 into v_range;
                    if v_sisa_pkp <= (v_range.maximum-v_range.minimum+1) then
                        v_pph21 = v_pph21 + (v_sisa_pkp * v_range.rate / 100); 
                    else
                        v_pph21 = v_pph21 + (v_range.maximum-v_range.minimum+1) * v_range.rate / 100;
                        v_sisa_pkp = v_sisa_pkp-(v_range.maximum-v_range.minimum+1);
                        select * from aag_master_pkp limit 1 offset 2 into v_range;
                        if v_sisa_pkp <= (v_range.maximum-v_range.minimum+1) then
                            v_pph21 = v_pph21 + v_sisa_pkp*v_range.rate/100;
                        else
                            v_pph21 = v_pph21 + (v_range.maximum-v_range.minimum+1)*v_range.rate/100;
                            v_sisa_pkp = v_sisa_pkp-(v_range.maximum-v_range.minimum+1);
                            select * from aag_master_pkp limit 1 offset 3 into v_range;
                            v_pph21 = v_pph21 + v_sisa_pkp*v_range.rate/100;
                        end if;
                    end if; 
 
                end if;  -- end level-1

                UPDATE aag_pph21_detail 
                    set b02tpp = v_pph21,
                    b08bru = v_b08bru,
                    b09jab = v_b09jab,
                    b11jpe = v_b11jpe,
                    b12net = v_b12net,
                    b14npp = v_b14npp,
                    b16pkp = v_b16pkp,
                    b17pph = v_pph21,
                    b19hut = v_pph21,
                    b20lns = v_pph21  
                    where id = v_detail.id;

                return v_pph21;
            END;
            $BODY$;

        """)

    def action_generate(self):
        cr = self.env.cr
        company_id=self.env['res.company']._company_default_get('hr.employee').id
        sql = "select aag_hitung_pph(%s,%s)"
        cr.execute(sql, (self.id,company_id))

    def action_export(self):
        start = time.time()

        self.export_filename  = 'Export-%s.csv' % time.strftime("%Y%m%d_%H%M%S")
        cr = self.env.cr
        sql = self.generate_sql()
        _logger.info('sql=%s', sql)
        cmd = ['psql']
        cmd.append('--command='+sql)
        cmd.append(cr.dbname)
        odoo.tools.exec_pg_command(*cmd)

        i=0
        fo = open(self.tmp_dir + self.export_filename, "rb")
        self.export_file = base64.b64encode(fo.read())
        fo.close()
        end = time.time()
        self.total_durations = end-start

    def generate_sql(self):
        sql="""\COPY (
        select 
        aimspj as "Masa Pajak",
        aithpj as "Tahun Pajak"
        from aag_pph21_detail where header_id=%s
        ) TO '%s' WITH (FORMAT CSV, HEADER TRUE, DELIMITER ';')
        """ %(self.id, self.tmp_dir+self.export_filename)
        return sql

    def action_export2(self):
        file_data = BytesIO()
        workbook = xlsxwriter.Workbook(file_data)
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': True})
        font12 = workbook.add_format({'bold': True, 'font_size': 12})
        font14 = workbook.add_format({'bold': True, 'font_size': 14})
        numeric = workbook.add_format({'num_format': '#,##0'})
        numeric2 = workbook.add_format({'num_format': '#,##0.00'})

        # SET COLUMN WIDTH
        worksheet.set_column('B:B', 8)  # Column  B width set to 10.
        worksheet.set_column('C:C', 30)  # Columns C width set to 30.
        worksheet.set_column('D:D', 6)  
        worksheet.set_column('E:E', 6)  
        worksheet.set_column('F:F', 6)  
        worksheet.set_column('G:G', 35)  
        worksheet.set_column('H:H', 12)  
        worksheet.set_column('I:I', 9)  
        worksheet.set_column('J:J', 9)  
        worksheet.set_column('K:K', 9)  
        worksheet.set_column('L:L', 9)  
        worksheet.set_column('M:M', 12)  
        worksheet.set_column('N:N', 12)  
        worksheet.set_column('O:O', 14)  
        worksheet.set_column('P:P', 12)  
        worksheet.set_column('Q:Q', 14)  
        worksheet.set_column('R:R', 12)  
        worksheet.set_column('S:S', 8)  
        worksheet.set_column('T:T', 8)  
        worksheet.set_column('U:U', 8)  
        worksheet.set_column('V:V', 8)  
        worksheet.set_column('W:W', 12)  
        worksheet.set_column('X:X', 12)  
        worksheet.set_column('Y:Y', 12)  
        worksheet.set_column('Z:Z', 12)  
        worksheet.set_column('AA:AA', 12)  
        worksheet.set_column('AB:AB', 10)  
        worksheet.set_column('AC:AC', 10)  
        worksheet.set_column('AD:AD', 12)  
        worksheet.set_column('AE:AE', 12)  
        worksheet.set_column('AF:AF', 14)  
        worksheet.set_column('AG:AG', 12)  
        worksheet.set_column('AH:AH', 12)  
        worksheet.set_column('AI:AI', 12)  
        worksheet.set_column('AJ:AJ', 16)  
        worksheet.set_column('AK:AK', 12)  
        worksheet.set_column('AL:AL', 12)  
        worksheet.set_column('AM:AM', 12)  
        worksheet.set_column('AN:AN', 12)  
        worksheet.set_column('AO:AO', 12)  
        worksheet.set_column('AP:AP', 12)  
        worksheet.set_column('AQ:AQ', 16)  
        worksheet.set_column('AR:AR', 12)  
        worksheet.set_column('AS:AS', 12)  
        worksheet.set_column('AT:AT', 8)  
        worksheet.set_column('AU:AU', 7)  
        worksheet.set_column('AV:AV', 15)  
        worksheet.set_column('AW:AW', 15)  
        worksheet.set_column('AX:AX', 25)  
        worksheet.set_column('AY:AY', 18)  
        worksheet.set_column('AZ:AZ', 25)  
        worksheet.set_column('BA:BA', 10)  
        worksheet.set_column('BB:BB', 10)  
        worksheet.set_column('BC:BC', 10)  
        worksheet.set_column('BD:BD', 10)  
        worksheet.set_column('BE:BE', 20)  

        # write header
        worksheet.write("B2", "PT. XACTI INDONESIA", font14)
        worksheet.write("B3", "Monthly Salary Detail Report", font12)

        worksheet.write("B5", "IDNO", bold)
        worksheet.write("C5", "NAME", bold)
        worksheet.write("D5", "DEPT", bold)
        worksheet.write("E5", "SECT", bold)
        worksheet.write("F5", "SBSEC", bold)
        worksheet.write("G5", "DESC", bold)
        worksheet.write("H5", "BASIC", bold)
        worksheet.write("I5", "I-BASIC", bold)
        worksheet.write("J5", "I-THR", bold)
        worksheet.write("K5", "I-BONUS", bold)
        worksheet.write("L5", "I-TPK", bold)
        worksheet.write("M5", "I-OCCUP", bold)
        worksheet.write("N5", "I-FAMILY", bold)
        worksheet.write("O5", "I-FUNCTIONAL", bold)
        worksheet.write("P5", "I-MEDICAL", bold)
        worksheet.write("Q5", "I-TRANSPORT", bold)
        worksheet.write("R5", "I-PERFORM", bold)
        worksheet.write("S5", "I-MEAL", bold)
        worksheet.write("T5", "I-SHIFT", bold)
        worksheet.write("U5", "I-LEAVE", bold)
        worksheet.write("V5", "I-OTHER", bold)
        worksheet.write("W5", "I-OVERTIME", bold)
        worksheet.write("X5", "I-RSGALLW", bold)
        worksheet.write("Y5", "I-DONATION", bold)
        worksheet.write("Z5", "I-PRVROUND", bold)
        worksheet.write("AA5", "I-PPH_DTP", bold)
        worksheet.write("AB5", "D-LOAN", bold)
        worksheet.write("AC5", "D-SPMI", bold)
        worksheet.write("AD5", "D-KOPERASI", bold)
        worksheet.write("AE5", "D-BASIC", bold)
        worksheet.write("AF5", "D-TRANSPORT", bold)
        worksheet.write("AG5", "D-OTHER", bold) 
        worksheet.write("AH5", "D-MEDICAL", bold)
        worksheet.write("AI5", "D-JHTEMP", bold)
        worksheet.write("AJ5", "D-BPJSKES_EMP", bold)
        worksheet.write("AK5", "D-PENEMP", bold)
        worksheet.write("AL5", "D-CURRND", bold)
        worksheet.write("AM5", "C-PPH21", bold)
        worksheet.write("AN5", "C-JHTCOM", bold)
        worksheet.write("AO5", "C-ACCCOM", bold)
        worksheet.write("AP5", "C-DTHCOM", bold)
        worksheet.write("AQ5", "C-BPJSKES_COM", bold)
        worksheet.write("AR5", "C-PENCOM", bold)
        worksheet.write("AS5", "NET", bold)
        worksheet.write("AT5", "EMPSTS", bold)
        worksheet.write("AU5", "DIRECT", bold)
        worksheet.write("AV5", "MED. BALANCE", bold)
        worksheet.write("AW5", "LEAVE BALANCE", bold)
        worksheet.write("AX5", "DEPT. GROUP-1", bold)
        worksheet.write("AY5", "DEPT. GROUP-2", bold)
        worksheet.write("AZ5", "DEPT. GROUP-3", bold)
        worksheet.write("BA5", "DEPT. GROUP-4", bold)
        worksheet.write("BB5", "MALE", bold)
        worksheet.write("BC5", "FEMALE", bold)
        worksheet.write("BD5", "GRADE", bold)
        worksheet.write("BE5", "POSITION", bold)

        # write data 
        row = 5
        for line in self.detail_ids:
            worksheet.write(row, 1, line.IDNO)
            worksheet.write(row, 2, line.NAME)
            worksheet.write(row, 3, line.DEPT)
            worksheet.write(row, 4, line.SECT)
            worksheet.write(row, 5, line.SBSEC)
            worksheet.write(row, 6, line.DESC)
            worksheet.write(row, 7, line.BASIC, numeric)
            worksheet.write(row, 8, line.I_BASIC, numeric)
            worksheet.write(row, 9, line.I_THR, numeric)
            worksheet.write(row, 10, line.I_BONUS, numeric)
            worksheet.write(row, 11, line.I_TPK, numeric)
            worksheet.write(row, 12, line.I_OCCUP, numeric)
            worksheet.write(row, 13, line.I_FAMILY, numeric)
            worksheet.write(row, 14, line.I_FUNCTIONAL, numeric)
            worksheet.write(row, 15, line.I_MEDICAL, numeric) 
            worksheet.write(row, 16, line.I_TRANSPORT, numeric)
            worksheet.write(row, 17, line.I_PERFORM, numeric)
            worksheet.write(row, 18, line.I_MEAL, numeric)
            worksheet.write(row, 19, line.I_SHIFT, numeric)
            worksheet.write(row, 20, line.I_LEAVE, numeric)
            worksheet.write(row, 21, line.I_OTHER, numeric)
            worksheet.write(row, 22, line.I_OVERTIME, numeric)
            worksheet.write(row, 23, line.I_RSGALLW, numeric)
            worksheet.write(row, 24, line.I_DONATION, numeric)
            worksheet.write(row, 25, line.I_PRVROUND, numeric)
            worksheet.write(row, 26, line.I_PPH_DTP, numeric)
            worksheet.write(row, 27, line.D_LOAN, numeric)
            worksheet.write(row, 28, line.D_SPMI, numeric)
            worksheet.write(row, 29, line.D_KOPERASI, numeric)
            worksheet.write(row, 30, line.D_BASIC, numeric)
            worksheet.write(row, 31, line.D_TRANSPORT, numeric)
            worksheet.write(row, 32, line.D_OTHER, numeric)
            worksheet.write(row, 33, line.D_MEDICAL, numeric)
            worksheet.write(row, 34, line.D_JHTEMP, numeric)
            worksheet.write(row, 35, line.D_BPJSKES_EMP, numeric)
            worksheet.write(row, 36, line.D_PENEMP, numeric)
            worksheet.write(row, 37, line.D_CURRND, numeric)
            worksheet.write(row, 38, line.C_PPH21, numeric)
            worksheet.write(row, 39, line.C_JHTCOM, numeric)
            worksheet.write(row, 40, line.C_ACCCOM, numeric)
            worksheet.write(row, 41, line.C_DTHCOM, numeric)
            worksheet.write(row, 42, line.C_BPJSKES_COM, numeric)
            worksheet.write(row, 43, line.C_PENCOM, numeric)
            worksheet.write(row, 44, line.NET, numeric)
            worksheet.write(row, 45, line.EMPSTS)
            worksheet.write(row, 46, line.DIRECT)
            worksheet.write(row, 47, line.MED_BALANCE, numeric)
            worksheet.write(row, 48, line.LEAVE_BALANCE, numeric2)
            worksheet.write(row, 49, line.GROUP_1)
            worksheet.write(row, 50, line.GROUP_2)
            worksheet.write(row, 51, line.GROUP_3)
            worksheet.write(row, 52, line.GROUP_4)
            worksheet.write(row, 53, line.x_male)
            worksheet.write(row, 54, line.x_female)
            worksheet.write(row, 55, line.ALLCD)
            worksheet.write(row, 56, line.POSIT)
            row += 1

        workbook.close()

        file_data.seek(0)
        self.export_file = base64.encodestring(file_data.getvalue())
        self.export_filename = 'report_payroll-%s-%s.xlsx' % (self.month, self.year)

        #_logger.info("--- action_export")


class report_detail(models.Model):
    _name           = 'aag.pph21_detail'
    _description    = 'PPh21 detail'

    header_id       = fields.Many2one(comodel_name="aag.pph21_header")

    idno            = fields.Integer("IDNO")
    # Field2 Berikut sesuai Form 1721-A1 (Bukti Potong)

    # Kelompok A (Identitas Penerima Penghasilan Yang Dipotong)
    aimspj          = fields.Integer("Masa Pajak")
    aithpj          = fields.Integer("Tahun Pajak")
    aipemb          = fields.Integer("Pembetulan")
    ainobp          = fields.Char("No Bukti Potong")
    aimsp1          = fields.Integer("Masa Perolehan-1")
    aimsp2          = fields.Integer("Masa Perolehan-2")
    ainppg          = fields.Char("NPWP Pegawai")
    ainipg          = fields.Char("NIK Pegawai")
    ainama          = fields.Char("Nama Pegawai")
    aialam          = fields.Char("Alamat Pegawai")
    aijkel          = fields.Char("Kode Jenis Kelamin")
    aisptk          = fields.Char("Status PTKP")
    aitang          = fields.Integer("Jumlah Tanggungan Kel.")
    aijbpg          = fields.Char("Jabatan Pegawai")
    aiwpln          = fields.Char("WP Luar Negeri")
    aikneg          = fields.Char("Kode Negara")

    # Kelompok B (Rincian Penghasilan dan Penghitungan PPh Pasal 21)
    bkdpjk          = fields.Char("Kode Objek Pajak")
    # Penghasilan Bruto:
    b01gji          = fields.Integer("Gaji/Pensiun atau THT/JHT")
    b02tpp          = fields.Integer("Tunjangan Pajak")
    b03tll          = fields.Integer("Tunjangan Lain-lain")
    b04hnr          = fields.Integer("Honorarium dan Sejenisnya")
    b05pre          = fields.Integer("Premi Asuransi Yg dibayar Pemberi Kerja")
    b06nat          = fields.Integer("Kenikmatan Natura")
    b07bns          = fields.Integer("Tantiem/Bonus/THR")
    b08bru          = fields.Integer("Penghasilan Bruto (Jumlah 1-7)")
    # Pengurangan:
    b09jab          = fields.Integer("Biaya Jabatan")
    b10tht          = fields.Integer("Iuran JHT/THT")
    b11jpe          = fields.Integer("Jumlah Pengurang (9+10)")
    # Penghitungan PPh Pasal 21
    b12net          = fields.Integer("Penghasilah Netto (8-11)")
    b13nes          = fields.Integer("Penghasilan Netto Masa Sebelumnya")
    b14npp          = fields.Integer("Penghasilan Netto Setahun/disetahunkan")
    b15ptk          = fields.Integer("Penghasilan Tidak Kena Pajak")
    b16pkp          = fields.Integer("Penghasilan Kena Pajak")
    b17pph          = fields.Integer("PPh21")
    b18pps          = fields.Integer("PPh21 Masa Sebelumnya")
    b19hut          = fields.Integer("PPh21 Terhutang")
    b20lns          = fields.Integer("PPh21 Yg Dipotong/Dilunasi")
 
    # Kelompok C (Identitas Pemotong)
    cispin          = fields.Char("Status Pindah")
    cinpwp          = fields.Char("NPWP")
    cinama          = fields.Char("Nama")
    citgbp          = fields.Char("Tanggal Bukti Potong")

    



