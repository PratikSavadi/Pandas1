import pandas
import os
import shutil
import datetime
import zipfile
import re
import glob
class GenerateUpiReport():
    def __init__(self):
        pass

    def getUpiReport(self,query):
        print 'alare'
	print query
        date= query['date']
        newPath = '/usr/share/nginx/smartrecon/mft/'
        if not os.path.exists(newPath + query['fname'].split('_')[0] + '_' + 'REPORT' + '/' + query['date']):
            print "========================="
            print newPath
        if not os.path.exists(newPath + query['fname'].split('_')[0] + '_' + 'REPORT'):
               os.mkdir(newPath + query['fname'].split('_')[0] + '_' + 'REPORT')
        if not os.path.exists(newPath + query['fname'].split('_')[0] + '_' + 'REPORT'+'/'+ query['date']):
                os.mkdir(newPath + query['fname'].split('_')[0] + '_' + 'REPORT'+'/'+ query['date'])

        if os.path.exists(newPath + query['fname'].split('_')[0] + '_' + 'REPORT' + '/' + query['date']):
            shutil.rmtree(newPath + query['fname'].split('_')[0] + '_' + 'REPORT' + '/' + query['date'])
            os.mkdir(newPath + query['fname'].split('_')[0] + '_' + 'REPORT' + '/' + query['date'])

            shutil.copy(query['path'] + query['fname'],
                        newPath + query['fname'].split('_')[0] + '_' + 'REPORT' + '/' + query['date'])
        readPath = newPath + query['fname'].split('_')[0] + '_' + 'REPORT' + '/' + query['date']
        print readPath
        # reqDate = str(datetime.date.today())

        path = readPath + '/' + query['fname']
        dest = readPath
       

        with zipfile.ZipFile(path, 'r') as zf:
            listOfFileNames = zf.namelist()
            for fileName in listOfFileNames:
	
                if fileName.endswith('.xls'):
                    zf.extract(fileName, dest)

        if os.path.exists(dest):
	    filelist=[]
            files = os.listdir(dest)
	    print files
	   
	    for i in files:
                if i.endswith('.xls'):
                     filelist.append(i)

            file = [i for i in filelist if re.match('[A-Z]{3}_[A-Z]{7}[0-9]{6}_[0-9]{1}C', i)]
	   
        else:
            print("no execution found")
        dfnew = pandas.DataFrame()
        C1 = False
        C2 = False
        C3 = False
        C4 = False
        upi=[]
        for a in file:
	    print a
            dfold= pandas.read_html(dest +'/'+ a,header=0)
	    print dfold 
             
       	    df=pandas.DataFrame(dfold[3])
	    #df = df[1:]
          
       	    #df.columns = ['Description', ' No of Txns', 'Debit', 'Credit']
       	    
            print df.columns
	     
            df['Description']=df['Description'].fillna('0')
	    df['Debit']=df['Debit'].fillna(0.0)
	    df['Credit']=df['Credit'].fillna(0.0)
	     
	    cycle = a.split('.')[0].split('_')[-1]
            dt = '-DT-'
#            cycle = df["cycle"].unique()
            date = a.split('_')[1][-6:]

#            df.drop(['No of Txns'], axis=1, inplace=True)

            dict1 = {'Rem SOD U2 Fee': ['Remitter SOD U2 Approved Fee', 'Remitter SOD U2 Approved NPCI Switching Fee'],
                     'Rem SOD U2 Fee Gst': ['Remitter SOD U2 Approved Fee GST',
                                            'Remitter SOD U2 Approved NPCI Switching Fee GST'],
                     'Rem SOD U3 Fee': ['Remitter SOD U3 Approved Fee', 'Remitter SOD U3 Approved NPCI Switching Fee'],
                     'Rem SOD U3 Fee Gst': ['Remitter SOD U3 Approved Fee GST',
                                            'Remitter SOD U3 Approved NPCI Switching Fee GST'],
                     'Rem SOD U2 Tran Amt': ['Remitter SOD U2 Approved Transaction Amount'],
                     'Rem SOD U3RB Fee': ['Remitter SOD U3-RB Approved Fee',
                                          'Remitter SOD U3-RB Approved NPCI Switching Fee'],
                     'Rem SOD U3 Tran Amt': ['Remitter SOD U3 Approved Transaction Amount'],
                     'Rem U2 Fee': ['Remitter U2 Approved Fee', 'Remitter U2 Approved NPCI Switching Fee'],
                     'Rem SOD U3RB Fee Gst': ['Remitter SOD U3-RB Approved Fee GST',
                                              'Remitter SOD U3-RB Approved NPCI Switching Fee GST'],
                     'Rem SOD U3RB Tran Amt': ['Remitter SOD U3-RB Approved Transaction Amount'],
                     'Rem U2 Fee Gst': ['Remitter U2 Approved Fee GST', 'Remitter U2 Approved NPCI Switching Fee GST'],
                     'REM U2 Tran Amt': ['Remitter U2 Approved Transaction Amount'],
                     'REM U3 Fee': ['Remitter U3 Approved Fee', 'Remitter U3 Approved NPCI Switching Fee'],
                     'Rem U3 Fee Gst': ['Remitter U3 Approved Fee GST', 'Remitter U3 Approved NPCI Switching Fee GST'],
                     'REM U3 Tran Amt': ['Remitter U3 Approved Transaction Amount'],
                     'REM U2RB Fee': ['Remitter U3-RB Approved Fee', 'Remitter U3-RB Approved NPCI Switching Fee'],
                     'REM U2RB Fee Gst': ['Remitter U3-RB Approved Fee GST',
                                          'Remitter U3-RB Approved NPCI Switching Fee GST'],
                     'REM U2RB Tran Amt': ['Remitter U3-RB Approved Transaction Amount'],
                     'REM UODU2 Fee': ['Remitter UOD U2 Approved Fee', 'Remitter UOD U2 Approved NPCI Switching Fee'],
                     'REM UODU2 Fee Gst': ['Remitter UOD U2 Approved Fee GST',
                                           'Remitter UOD U2 Approved NPCI Switching Fee GST'],
                     'REM UODU2 Tran Amt': ['Remitter UOD U2 Approved Transaction Amount'],
                     'SOD U3 PSP Fee': ['SOD U3 Approved Payer PSP Fee - Paid'],
                     'SOD U3 PSP Fee Gst': ['SOD U3 Approved Payer PSP Fee GST - Paid'],
                     'U2 PSP Fee': ['U2 Approved Payer PSP Fee - Paid'],
                     'U2 PSP Fee Gst': ['U2 Approved Payer PSP Fee GST - Paid'],
                     'U3 PSP Fee': ['U3 Approved Payer PSP Fee - Paid'],
                     'SOD U3RB PSP Fee': ['SOD U3-RB Approved Payer PSP Fee - Paid'],
                     'SOD U3RB PSP Fee Gst': ['SOD U3-RB Approved Payer PSP Fee GST - Paid'],
                     'U3 PSP Fee Gst': ['U3 Approved Payer PSP Fee GST - Paid'],
                     'U3RB PSP Fee': ['U3-RB Approved Payer PSP Fee - Paid'],
                     'U3RB PSP Fee Gst': ['U3-RB Approved Payer PSP Fee GST - Paid'],
                     'UODU2 PSP Fee': ['UOD U2 Approved Payer PSP Fee - Paid'],
                     'UODU2 PSP Fee Gst': ['UOD U2 Approved Payer PSP Fee GST - Paid'],
                     'BEN Fin-BBPS U2 Fee': ['Beneficiary Fin-BBPS U2 Approved Fee',
                                             'Beneficiary Fin-BBPS U2 Approved NPCI Switching Fee'],
                     'BEN Fin-BBPS U2 Fee Gst': ['Beneficiary Fin-BBPS U2 Approved Fee GST',
                                                 'Beneficiary Fin-BBPS U2 Approved NPCI Switching Fee GST'],
                     'BEN Fin-BBPS U2 Tran Amt': ['Beneficiary Fin-BBPS U2 Approved Transaction Amount'],
                     'Ben SOD U2 Fee': ['Beneficiary SOD U2 Approved Fee',
                                        'Beneficiary SOD U2 Approved NPCI Switching Fee'],
                     'Ben SOD U2 Fee Gst': ['Beneficiary SOD U2 Approved Fee GST',
                                            'Beneficiary SOD U2 Approved NPCI Switching Fee GST'],
                     'Ben SOD U2 Tran Amt': ['Beneficiary SOD U2 Approved Transaction Amount'],
                     'Ben U2 Fee': ['Beneficiary U2 Approved Fee', 'Beneficiary U2 Approved NPCI Switching Fee'],
                     'Ben U2 Fee Gst': ['Beneficiary U2 Approved Fee GST',
                                        'Beneficiary U2 Approved NPCI Switching Fee GST'],
                     'Ben U2 Tran Amt': ['Beneficiary U2 Approved Transaction Amount'],
                     'Ben U3 Fee': ['Beneficiary U3 Approved Fee'],
                     'Ben U3 Fee Gst': ['Beneficiary U3 Approved Fee GST'],
                     'Ben U3 Tran Amt': ['Beneficiary U3 Approved Transaction Amount'],
                     'Ben SOD U3 Fee': ['Beneficiary SOD U3 Approved Fee'],
                     'Ben SOD U3 Fee Gst': ['Beneficiary SOD U3 Approved Fee GST'],
                     'Ben SOD U3 Tran Amt': ['Beneficiary SOD U3 Approved Transaction Amount'],
                     'Ben U3RB Fee': ['Beneficiary U3-RB Approved Fee'],
                     'Ben U3RB Fee Gst': ['Beneficiary U3-RB Approved Fee GST'],
                     'U3 PSP Fee Recv': ['U3 Approved Payer PSP Fee - Received'],
                     'U3 PSP Fee Gst Recv': ['U3 Approved Payer PSP Fee GST - Received'],
                     'Ben U3RB Tran Amt': ['Beneficiary U3-RB Approved Transaction Amount'],
                     'Ben SOD U2RB Fee': ['Beneficiary SOD U2-RB Approved Fee',
                                          'Beneficiary SOD U2-RB Approved NPCI Switching Fee'],
                     'Ben SOD U2RB Fee Gst': ['Beneficiary SOD U2-RB Approved Fee GST',
                                              'Beneficiary SOD U2-RB Approved NPCI Switching Fee GST'],
                     'Ben SOD U2RB Tran Amt': ['Beneficiary SOD U2-RB Approved Transaction Amount'],
		     'Final Settlement Amount':['Final Settlement Amount'],'Net Adjusted Amount': ['Net Adjusted Amount'],
	             'Net Adjusted Fee with Tax': ['Net Adjusted Fee with Tax']}
            # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
            GLACdeb = {'Rem SOD U2 Fee': '404210037', 'Rem SOD U2 Fee Gst': '114070217',
                       'Rem SOD U2 Tran Amt': '200000120275', 'Rem SOD U3 Fee': '404210037',
                       'Rem SOD U3 Fee Gst': '114070217', 'Rem SOD U3 Tran Amt': '200000120275',
                       'Rem U2 Fee': '404210037', 'Rem U2 Fee Gst': '114070217', 'REM U2 Tran Amt': '200000120275',
                       'REM U3 Fee': '404210037',
                       'Rem U3 Fee Gst': '114070217', 'REM U3 Tran Amt': '200000120275', 'REM U2RB Fee': '404210037',
                       'REM U2RB Fee Gst': '114070217', 'REM U2RB Tran Amt': '200000120275',
                       'REM UODU2 Fee': '404210037', 'REM UODU2 Fee Gst': '114070217',
                       'REM UODU2 Tran Amt': '200000120275', 'Rem SOD U3RB Fee': '404210037',
                       'Rem SOD U3RB Fee Gst': '114070217', 'Rem SOD U3RB Tran Amt': '200000120275',
                       'SOD U3 PSP Fee': '404210037', 'SOD U3 PSP Fee Gst': '114070217', 'U2 PSP Fee': '404210037',
                       'U2 PSP Fee Gst': '114070217', 'U3 PSP Fee': '404210037', 'U3 PSP Fee Gst': '114070217',
                       'U3RB PSP Fee': '404210037', 'U3RB PSP Fee Gst': '114070217', 'UODU2 PSP Fee': '404210037',
                       'UODU2 PSP Fee Gst': '114070217', 'SOD U3RB PSP Fee': '404210037',
                       'SOD U3RB PSP Fee Gst': '114070217',
                       'BEN Fin-BBPS U2 Fee': '404210037', 'BEN Fin-BBPS U2 Fee Gst': '114070217',
                       'BEN Fin-BBPS U2 Tran Amt': '200000120275', 'Ben SOD U2 Fee': '404210037',
                       'Ben SOD U2 Fee Gst': '114070217', 'Ben SOD U2 Tran Amt': '200000120275',
                       'Ben U2 Fee': '404210037', 'Ben U2 Fee Gst': '114070217', 'Ben U2 Tran Amt': '200000120275',
                       'Ben U3 Fee': '404210037', 'Ben U3 Fee Gst': '114070217', 'Ben U3 Tran Amt': '200000120275',
                       'Ben SOD U3 Fee': '404210037', 'Ben SOD U3 Fee Gst': '114070217',
                       'Ben SOD U3 Tran Amt': '200000120275', 'Ben U3RB Fee': '404210037',
                       'Ben U3RB Fee Gst': '114070217', 'Ben U3RB Tran Amt': '200000120275',
                       'Ben SOD U2RB Fee': '404210037', 'Ben SOD U2RB Fee Gst': '114070217',
                       'Ben SOD U2RB Tran Amt': '200000120275','Final Settlement Amount':'110040003',
		       'Net Adjusted Amount': '200000120275', 'Net Adjusted Fee with Tax': '114070217'}


            AcNamedeb = {'Rem SOD U2 Fee': 'UPI expense A/c', 'Rem SOD U2 Fee Gst': 'IGST RECOVERY- FLEX',
                         'Rem SOD U2 Tran Amt': 'UPI OUTWARD ACCOUNT', 'Rem SOD U3 Fee': 'UPI expense A/c',
                         'Rem SOD U3 Fee Gst': 'IGST RECOVERY- FLEX', 'Rem SOD U3 Tran Amt': 'UPI OUTWARD ACCOUNT',
                         'Rem U2 Fee': 'UPI expense A/c', 'Rem U2 Fee Gst': 'IGST RECOVERY- FLEX',
                         'REM U2 Tran Amt': 'UPI OUTWARD ACCOUNT', 'REM U3 Fee': 'UPI expense A/c',
                         'Rem U3 Fee Gst': 'IGST RECOVERY- FLEX', 'REM U3 Tran Amt': 'UPI OUTWARD ACCOUNT',
                         'REM U2RB Fee': 'UPI expense A/c', 'REM U2RB Fee Gst': 'IGST RECOVERY- FLEX',
                         'Rem SOD U3RB Fee': 'UPI expense A/c', 'Rem SOD U3RB Fee Gst': 'IGST RECOVERY- FLEX',
                         'Rem SOD U3RB Tran Amt': 'UPI OUTWARD ACCOUNT',
                         'REM U2RB Tran Amt': 'UPI OUTWARD ACCOUNT', 'REM UODU2 Fee': 'UPI expense A/c',
                         'REM UODU2 Fee Gst': 'IGST RECOVERY- FLEX', 'REM UODU2 Tran Amt': 'UPI OUTWARD ACCOUNT',
                         'SOD U3 PSP Fee': 'UPI expense A/c', 'SOD U3 PSP Fee Gst': 'IGST RECOVERY- FLEX',
                         'U2 PSP Fee': 'UPI expense A/c', 'U2 PSP Fee Gst': 'IGST RECOVERY- FLEX',
                         'U3 PSP Fee': 'UPI expense A/c', 'U3 PSP Fee Gst': 'IGST RECOVERY- FLEX',
                         'U3RB PSP Fee': 'UPI expense A/c', 'U3RB PSP Fee Gst': 'IGST RECOVERY- FLEX',
                         'UODU2 PSP Fee': 'UPI expense A/c', 'UODU2 PSP Fee Gst': 'IGST RECOVERY- FLEX',
                         'SOD U3RB PSP Fee': 'UPI expense A/c', 'SOD U3RB PSP Fee Gst': 'IGST RECOVERY- FLEX',
                         'BEN Fin-BBPS U2 Fee': 'UPI expense A/c', 'BEN Fin-BBPS U2 Fee Gst': 'IGST RECOVERY- FLEX',
                         'BEN Fin-BBPS U2 Tran Amt': 'UPI OUTWARD ACCOUNT', 'Ben SOD U2 Fee': 'UPI expense A/c',
                         'Ben SOD U2 Fee Gst': 'IGST RECOVERY- FLEX', 'Ben SOD U2 Tran Amt': 'UPI OUTWARD ACCOUNT',
                         'Ben U2 Fee': 'UPI expense A/c', 'Ben U2 Fee Gst': 'IGST RECOVERY- FLEX',
                         'Ben U2 Tran Amt': 'UPI OUTWARD ACCOUNT', 'Ben U3 Fee': 'UPI expense A/c',
                         'Ben U3 Fee Gst': 'IGST RECOVERY- FLEX', 'Ben U3 Tran Amt': 'UPI OUTWARD ACCOUNT',
                         'Ben SOD U3 Fee': 'UPI expense A/c',
                         'Ben SOD U3 Fee Gst': 'IGST RECOVERY- FLEX', 'Ben SOD U3 Tran Amt': 'UPI OUTWARD ACCOUNT',
                         'Ben U3RB Fee': 'UPI expense A/c', 'Ben U3RB Fee Gst': 'IGST RECOVERY- FLEX',
                         'Ben U3RB Tran Amt': 'UPI OUTWARD ACCOUNT', 'Ben SOD U2RB Fee': 'UPI expense A/c',
                         'Ben SOD U2RB Fee Gst': 'IGST RECOVERY- FLEX',
                         'Ben SOD U2RB Tran Amt': 'UPI OUTWARD ACCOUNT','Final Settlement Amount':'RTGS SETTLEMENT ACCOUNT WITH RBI' ,
			 'Net Adjusted Amount': 'UPI OUTWARD ACCOUNT', 'Net Adjusted Fee with Tax': 'IGST RECOVERY- FLEX'}

            Narrationdeb = {'Rem SOD U2 Fee': 'UPI REM SOD U2 APP Fee',
                            'Rem SOD U2 Fee Gst': 'UPI REM SOD U2 APP Fee IGST',
                            'Rem SOD U2 Tran Amt': 'UPI REM SOD U2 APP Txn Amt',
                            'Rem SOD U3 Fee': 'UPI REM SOD U3 APP Fee',
                            'Rem SOD U3 Fee Gst': 'UPI REM SOD U3 APP Fee IGST',
                            'Rem SOD U3 Tran Amt': 'UPI REM SOD U3 APP Txn Amt', 'Rem U2 Fee': 'UPI REM U2 APP Fee',
                            'Rem U2 Fee Gst': 'UPI REM U2 APP Fee GST',
                            'REM U2 Tran Amt': 'UPI REM U2 APP Transaction Amount', 'REM U3 Fee': 'UPI REM U3 APP Fee ',
                            'Rem U3 Fee Gst': 'UPI REM U3 APP Fee IGST', 'REM U3 Tran Amt': 'UPI REM U3 APP Txn Amt',
                            'REM U2RB Fee': 'UPI REM U3-RB APP Fee', 'REM U2RB Fee Gst': 'UPI REM U3-RB APP Fee IGST ',
                            'REM U2RB Tran Amt': 'UPI REM U3-RB APP Txn Amt', 'REM UODU2 Fee': 'UPI REM UOD U2 APP Fee',
                            'REM UODU2 Fee Gst': 'UPI REM UOD U2 APP Fee GST',
                            'REM UODU2 Tran Amt': 'UPI REM UOD U2 APP Transaction Amount',
                            'Rem SOD U3RB Fee': 'UPI REM SOD U3-RB APP Fee',
                            'Rem SOD U3RB Fee Gst': 'UPI REM SOD U3-RB APP Fee IGST',
                            'Rem SOD U3RB Tran Amt': 'UPI REM SOD U3-RB APP Txn Amt',
                            'SOD U3 PSP Fee': 'UPI SOD U3 APP Payer PSP Fee -Paid',
                            'SOD U3 PSP Fee Gst': 'UPI SOD U3 APP Payer PSP Fee IGST -Paid',
                            'U2 PSP Fee': 'UPI U2 APP Payer PSP Fee -Paid ',
                            'U2 PSP Fee Gst': 'UPI U2 APP Payer PSP Fee IGST -Paid ',
                            'UODU2 PSP Fee': 'UPI UOD U2 APP Payer PSP Fee -Paid',
                            'UODU2 PSP Fee Gst': 'UPI UOD U2 APP Payer PSP Fee IGST -Paid',
                            'SOD U3RB PSP Fee': 'UPI SOD U3-RB APP Payer PSP Fee -Paid',
                            'SOD U3RB PSP Fee Gst': 'UPI SOD U3-RB APP Payer PSP Fee IGST -Paid',
                            'U3 PSP Fee': 'UPI U3 APP Payer PSP Fee -Paid',
                            'U3 PSP Fee Gst': 'UPI U3 APP Payer PSP Fee IGST -Paid',
                            'U3RB PSP Fee': 'UPI U3-RB APP Payer PSP Fee -Paid',
                            'U3RB PSP Fee Gst': 'UPI U3-RB APP Payer PSP Fee IGST -Paid',
                            'BEN Fin-BBPS U2 Fee': 'UPI BEN Fin-BBPS U2 APP Fee',
                            'BEN Fin-BBPS U2 Fee Gst': 'UPI BEN Fin-BBPS U2 APP Fee GST',
                            'BEN Fin-BBPS U2 Tran Amt': 'UPI BEN Fin-BBPS U2 APP Transaction Amount',
                            'Ben SOD U2 Fee': 'UPI BEN SOD U2 APP Fee',
                            'Ben SOD U2 Fee Gst': 'UPI BEN SOD U2 APP Fee GST',
                            'Ben SOD U2 Tran Amt': 'UPI BEN SOD U2 APP Transaction Amount',
                            'Ben U2 Fee': 'UPI BEN U2 APP Fee',
                            'Ben U2 Tran Amt': 'UPI BEN U2 APP Transaction Amount',
                            'Ben U2 Fee Gst': 'UPI BEN U2 APP Fee GST', 'Ben U3 Fee': 'UPI BEN U3 APP Fee',
                            'Ben U3 Fee Gst': 'UPI BEN U3 APP Fee GST',
                            'Ben U3 Tran Amt': 'UPI BEN U3 APP Transaction Amount',
                            'Ben SOD U3 Fee': 'UPI BEN SOD U3 APP Fee',
                            'Ben SOD U3 Fee Gst': 'UPI BEN SOD U3 APP Fee GST ',
                            'Ben SOD U3 Tran Amt': 'UPI BEN SOD U3 APP Transaction Amount',
                            'Ben U3RB Fee': 'UPI BEN U3-RB APP Fee', 'Ben U3RB Fee Gst': 'UPI BEN U3-RB APP Fee GST',
                            'Ben U3RB Tran Amt': 'UPI BEN U3-RB APP Transaction Amount',
                            'Ben SOD U2RB Fee': 'UPI BEN SOD U2-RB APP Fee',
                            'Ben SOD U2RB Fee Gst': 'UPI BEN SOD U2-RB APP Fee GST',
                            'Ben SOD U2RB Tran Amt': 'UPI BEN SOD-RB U2 APP Transaction Amount','Final Settlement Amount':'UPI Final Settlement',
			    'Net Adjusted Amount': 'UPI Net Adjusted Amount','Net Adjusted Fee with Tax': 'UPI Net Adjusted Fee with Tax'}

            # ---------------------------------------------------------------------------------------------------------------------------------------------------------------
            GLACcred = {'Rem SOD U2 Fee': '302250016', 'Rem SOD U2 Fee Gst': '208080261',
                        'Rem SOD U2 Tran Amt': '200000120288', 'Rem SOD U3 Fee': '302250016',
                        'Rem SOD U3 Fee Gst': '208080261', 'Rem SOD U3 Tran Amt': '200000120288',
                        'Rem U2 Fee': '302250016', 'Rem U2 Fee Gst': '208080261', 'REM U2 Tran Amt': '200000120288',
                        'REM U3 Fee': '302250016',
                        'Rem U3 Fee Gst': '208080261', 'REM U3 Tran Amt': '200000120288', 'REM U2RB Fee': '302250016',
                        'REM U2RB Fee Gst': '208080261', 'REM U2RB Tran Amt': '200000120288',
                        'REM UODU2 Fee': '302250016', 'REM UODU2 Fee Gst': '208080261',
                        'REM UODU2 Tran Amt': '200000120288', 'Rem SOD U3RB Fee': '302250016',
                        'Rem SOD U3RB Fee Gst': '208080261', 'Rem SOD U3RB Tran Amt': '200000120288',
                        'U3 PSP Fee Recv': '302250016', 'U3 PSP Fee Gst Recv': '208080261',
                        'SOD U3 PSP Fee': '302250016', 'SOD U3 PSP Fee Gst': '208080261', 'U2 PSP Fee': '302250016',
                        'U2 PSP Fee Gst': '208080261', 'U3 PSP Fee': '302250016', 'U3 PSP Fee Gst': '208080261',
                        'U3RB PSP Fee': '302250016', 'U3RB PSP Fee Gst': '208080261', 'UODU2 PSP Fee': '302250016',
                        'UODU2 PSP Fee Gst': '208080261', 'SOD U3RB PSP Fee': '302250016',
                        'SOD U3RB PSP Fee Gst': '208080261',
                        'BEN Fin-BBPS U2 Fee': '302250016', 'BEN Fin-BBPS U2 Fee Gst': '208080261',
                        'BEN Fin-BBPS U2 Tran Amt': '200000120288', 'Ben SOD U2 Fee': '302250016',
                        'Ben SOD U2 Fee Gst': '208080261', 'Ben SOD U2 Tran Amt': '200000120288',
                        'Ben U2 Fee': '302250016', 'Ben U2 Fee Gst': '208080261', 'Ben U2 Tran Amt': '200000120288',
                        'Ben U3 Fee': '302250016', 'Ben U3 Fee Gst': '208080261', 'Ben U3 Tran Amt': '200000120288',
                        'Ben SOD U3 Fee': '302250016', 'Ben SOD U3 Fee Gst': '208080261',
                        'Ben SOD U3 Tran Amt': '200000120288', 'Ben U3RB Fee': '302250016',
                        'Ben U3RB Fee Gst': '208080261', 'Ben U3RB Tran Amt': '200000120288',
                        'Ben SOD U2RB Fee': '302250016', 'Ben SOD U2RB Fee Gst': '208080261',
                        'Ben SOD U2RB Tran Amt': '200000120288','Final Settlement Amount':'110040003',
		        'Net Adjusted Amount': '200000120288', 'Net Adjusted Fee with Tax': '208080261'}

            AcNamecred = {'Rem SOD U2 Fee': 'UPI INCOME A/C', 'Rem SOD U2 Fee Gst': 'GST LIABILITY- Flex',
                          'Rem SOD U2 Tran Amt': 'UPI INWARD ACCOUNT', 'Rem SOD U3 Fee': 'UPI INCOME A/C',
                          'Rem SOD U3 Fee Gst': 'GST LIABILITY- Flex', 'Rem SOD U3 Tran Amt': 'UPI INWARD ACCOUNT',
                          'Rem U2 Fee': 'UPI INCOME A/C', 'Rem U2 Fee Gst': 'GST LIABILITY- Flex',
                          'REM U2 Tran Amt': 'UPI INWARD ACCOUNT', 'REM U3 Fee': 'UPI INCOME A/C',
                          'Rem U3 Fee Gst': 'GST LIABILITY- Flex', 'REM U3 Tran Amt': 'UPI INWARD ACCOUNT',
                          'REM U2RB Fee': 'UPI INCOME A/C', 'REM U2RB Fee Gst': 'GST LIABILITY- Flex',
                          'Rem SOD U3RB Fee': 'UPI INCOME A/C', 'Rem SOD U3RB Fee Gst': 'GST LIABILITY- Flex',
                          'Rem SOD U3RB Tran Amt': 'UPI INWARD ACCOUNT',
                          'REM U2RB Tran Amt': 'UPI INWARD ACCOUNT', 'REM UODU2 Fee': 'UPI INCOME A/C',
                          'REM UODU2 Fee Gst': 'GST LIABILITY- Flex', 'REM UODU2 Tran Amt': 'UPI INWARD ACCOUNT',
                          'SOD U3 PSP Fee': 'UPI INCOME A/C', 'SOD U3 PSP Fee Gst': 'GST LIABILITY- Flex',
                          'U2 PSP Fee': 'UPI INCOME A/C', 'U2 PSP Fee Gst': 'GST LIABILITY- Flex',
                          'U3 PSP Fee': 'UPI INCOME A/C', 'U3 PSP Fee Gst': 'GST LIABILITY- Flex',
                          'U3RB PSP Fee': 'UPI INCOME A/C', 'U3RB PSP Fee Gst': 'GST LIABILITY- Flex',
                          'UODU2 PSP Fee': 'UPI INCOME A/C', 'UODU2 PSP Fee Gst': 'GST LIABILITY- Flex',
                          'SOD U3RB PSP Fee': 'UPI INCOME A/C', 'SOD U3RB PSP Fee Gst': 'GST LIABILITY- Flex',
                          'U3 PSP Fee Recv': 'UPI INCOME A/C', 'U3 PSP Fee Gst Recv': 'GST LIABILITY- Flex',
                          'BEN Fin-BBPS U2 Fee': 'UPI INCOME A/C', 'BEN Fin-BBPS U2 Fee Gst': 'GST LIABILITY- Flex',
                          'BEN Fin-BBPS U2 Tran Amt': 'UPI INWARD ACCOUNT', 'Ben SOD U2 Fee': 'UPI INCOME A/C',
                          'Ben SOD U2 Fee Gst': 'GST LIABILITY- Flex', 'Ben SOD U2 Tran Amt': 'UPI INWARD ACCOUNT',
                          'Ben U2 Fee': 'UPI INCOME A/C',
                          'Ben U2 Fee Gst': 'GST LIABILITY- Flex', 'Ben U2 Tran Amt': 'UPI INWARD ACCOUNT',
                          'Ben U3 Fee': 'UPI INCOME A/C', 'Ben U3 Fee Gst': 'GST LIABILITY- Flex',
                          'Ben U3 Tran Amt': 'UPI INWARD ACCOUNT',
                          'Ben SOD U3 Fee': 'UPI INCOME A/C', 'Ben SOD U3 Fee Gst': 'GST LIABILITY- Flex',
                          'Ben SOD U3 Tran Amt': 'UPI INWARD ACCOUNT', 'Ben U3RB Fee': 'UPI INCOME A/C',
                          'Ben U3RB Fee Gst': 'GST LIABILITY- Flex', 'Ben U3RB Tran Amt': 'UPI INWARD ACCOUNT',
                          'Ben SOD U2RB Fee': 'UPI INCOME A/C', 'Ben SOD U2RB Fee Gst': 'GST LIABILITY- Flex',
                          'Ben SOD U2RB Tran Amt': 'UPI INWARD ACCOUNT','Final Settlement Amount':'RTGS SETTLEMENT ACCOUNT WITH RBI',
	                  'Net Adjusted Amount': 'UPI INWARD ACCOUNT', 'Net Adjusted Fee with Tax': 'GST LIABILITY- Flex'}


            Narrationcred = {'Rem SOD U2 Fee': 'UPI REM SOD U2 APP Fee ',
                             'Rem SOD U2 Fee Gst': 'UPI REM SOD U2 APP Fee IGST',
                             'Rem SOD U2 Tran Amt': 'UPI REM SOD U2 APP Txn Amt',
                             'Rem SOD U3 Fee': 'UPI REM SOD U3 APP Fee ',
                             'Rem SOD U3 Fee Gst': 'UPI REM SOD U3 APP Fee IGST',
                             'Rem SOD U3 Tran Amt': 'UPI REM SOD U3 APP Txn Amt ', 'Rem U2 Fee': 'UPI REM U2 APP Fee',
                             'Rem U2 Fee Gst': 'UPI REM U2 APP Fee GST',
                             'REM U2 Tran Amt': 'UPI REM U2 APP Transaction Amount',
                             'REM U3 Fee': 'UPI REM U3 APP Fee ', 'Rem U3 Fee Gst': 'UPI REM U3 APP Fee IGST',
                             'REM U3 Tran Amt': 'UPI REM U3 APP Txn Amt', 'REM U2RB Fee': 'UPI REM U3-RB APP Fee ',
                             'REM U2RB Fee Gst': 'UPI REM U3-RB APP Fee IGST ',
                             'REM U2RB Tran Amt': 'UPI Remitter U3-RB APP Txn Amt ',
                             'Rem SOD U3RB Fee': 'UPI REM SOD U3-RB APP Fee ',
                             'Rem SOD U3RB Fee Gst': 'UPI REM SOD U3-RB APP Fee IGST',
                             'Rem SOD U3RB Tran Amt': 'UPI REM SOD U3-RB APP Txn Amt',
                             'REM UODU2 Fee': 'UPI REM UOD U2 APP Fee',
                             'REM UODU2 Fee Gst': 'UPI REM UOD U2 APP Fee GST',
                             'REM UODU2 Tran Amt': 'UPI REM UOD U2 APP Transaction Amount',
                             'U2 PSP Fee Gst': 'UPI U2 APP Payer PSP Fee IGST -Paid ',
                             'SOD U3 PSP Fee': 'UPI SOD U3 APP Payer PSP Fee -Paid ',
                             'SOD U3 PSP Fee Gst': 'UPI SOD U3 APP Payer PSP Fee IGST -Paid ',
                             'U2 PSP Fee': 'UPI U2 APP Payer PSP Fee -Paid ',
                             'U3 PSP Fee': 'UPI U3 APP Payer PSP Fee -Paid ',
                             'U3 PSP Fee Gst': 'UPI U3 APP Payer PSP Fee IGST -Paid ',
                             'SOD U3RB PSP Fee': 'UPI SOD U3-RB APP Payer PSP Fee -Paid ',
                             'SOD U3RB PSP Fee Gst': 'UPI SOD U3-RB APP Payer PSP Fee IGST -Paid',
                             'U3RB PSP Fee': 'UPI U3-RB APP Payer PSP Fee -Paid',
                             'U3RB PSP Fee Gst': 'UPI U3-RB APP Payer PSP Fee IGST -Paid ',
                             'UODU2 PSP Fee': 'UPI UOD U2 APP Payer PSP Fee -Paid',
                             'UODU2 PSP Fee Gst': 'UPI UOD U2 APP Payer PSP Fee IGST -Paid',
                             'U3 PSP Fee Recv': 'UPI U3 Approved Payer PSP Fee - Received',
                             'U3 PSP Fee Gst Recv': 'UPI U3 Approved Payer PSP Fee GST - Received',
                             'BEN Fin-BBPS U2 Fee': 'UPI BEN Fin-BBPS U2 APP Fee',
                             'BEN Fin-BBPS U2 Fee Gst': 'UPI BEN Fin-BBPS U2 APP Fee GST ',
                             'BEN Fin-BBPS U2 Tran Amt': 'UPI BEN Fin-BBPS U2 APP Transaction Amount ',
                             'Ben SOD U2 Fee': 'UPI BEN SOD U2 APP Fee ',
                             'Ben SOD U2 Fee Gst': 'UPI BEN SOD U2 APP Fee GST',
                             'Ben SOD U2 Tran Amt': 'UPI BEN SOD U2 APP Transaction Amount ',
                             'Ben U2 Fee': 'UPI BEN U2 APP Fee ', 'Ben U2 Fee Gst': 'UPI BEN U2 APP Fee GST',
                             'Ben U2 Tran Amt': 'UPI BEN U2 APP Transaction Amount',
                             'Ben U3 Fee': 'UPI BEN U3 APP Fee ', 'Ben U3 Fee Gst': 'UPI BEN U3 APP Fee GST ',
                             'Ben U3 Tran Amt': 'UPI BEN U3 APP Transaction Amount ',
                             'Ben SOD U3 Fee': 'UPI BEN SOD U3 APP Fee ',
                             'Ben SOD U3 Fee Gst': 'UPI BEN SOD U3 APP Fee GST ',
                             'Ben SOD U3 Tran Amt': 'UPI BEN SOD U3 APP Transaction Amount ',
                             'Ben U3RB Fee': 'UPI BEN U3-RB APP Fee', 'Ben U3RB Fee Gst': 'UPI BEN U3-RB APP Fee GST',
                             'Ben U3RB Tran Amt': 'UPI BEN U3-RB APP Transaction Amount ',
                             'Ben SOD U2RB Fee': 'UPI BEN SOD-RB U2 APP Fee ',
                             'Ben SOD U2RB Fee Gst': 'UPI BEN SOD-RB U2 APP Fee GST',
                             'Ben SOD U2RB Tran Amt': 'UPI BEN SOD-RB U2 APP Transaction Amount','Final Settlement Amount':'UPI Final Settlement',
        		     'Net Adjusted Amount': 'UPI  Net Adjusted Amount','Net Adjusted Fee with Tax': 'UPI Net Adjusted Fee with Tax'}


            Narrationcredben = {'Ben U2 Fee': 'UPI BEN U2 Approved NPCI Switching Fee',
                                'Ben U2 Fee Gst': 'UPI BEN U2 Approved NPCI Switching Fee IGst',
                                'BEN Fin-BBPS U2 Fee': 'UPI BEN Fin-BBPS U2 Approved NPCI Switching Fee',
                                'BEN Fin-BBPS U2 Fee Gst': 'UPI BEN Fin-BBPS U2 Approved NPCI Switching Fee IGST',
                                'Ben SOD U2 Fee': 'UPI BEN SOD U2 Approved NPCI Switching Fee',
                                'Ben SOD U2 Fee Gst': 'UPI BEN SOD U2 APP NPCI Switching Fee IGST',
                                'Ben SOD U2RB Fee': 'UPI BEN SOD U2-RB Approved NPCI Switching Fee',
                                'Ben SOD U2RB Fee Gst': 'UPI BEN SOD U2-RB APP NPCI Switching Fee IGST'}

            # -------------------------------------------------------------------------------------------------------------------------------------------------------------------
            maindf = pandas.DataFrame(columns=['GL AC', 'Ac Name', 'Dr', 'Narration'])
	    l1=[]
	    l2=[]
	    l=[]
	    for i,d in dict1.iteritems():
    		if len(i):
        	   l1.append(i)
    	        if len(d):
        	   l2.extend(d)
	    l=l1+l2
	    for i in df['Description']:
		if i not in l:
		    print i
		    
		    if i[0:3]!='Rem' and i[0:3]!='Ben':
			if '-' in i and 'Fee' in i  and 'Fee GST' not in i:
				dictKey =i.split(' ')[0]+' '+i.split(' ')[-4]+' '+i.split(' ')[-3]+' '+i.split(' ')[-2]+' '+i.split(' ')[-1]
				if dictKey not in dict1.keys():
					dict1[dictKey]=[]
                    			dict1[dictKey].append(str(i))
                    			GLACdeb[dictKey]='404210037'
                    			AcNamedeb[dictKey]='UPI expense A/c'
                    			Narrationdeb[dictKey]='UPI' + ' ' + str(i)
                    			GLACcred[dictKey]='302250016'
                    			AcNamecred[dictKey]='UPI INCOME A/C'
                    			Narrationcred[dictKey]='UPI' + ' ' + str(i)
			if '-' in i and 'Fee GST' in i:
				dictKey = i.split(' ')[0] + ' ' + i.split(' ')[-5]+ ' ' + i.split(' ')[-4] + ' ' + i.split(' ')[-3] + ' ' +i.split(' ')[-2] + ' ' + i.split(' ')[-1]
				if dictKey not in dict1.keys():
					dict1[dictKey] = []
                    			dict1[dictKey].append(str(i))
                    			GLACdeb[dictKey] = '114070217'
                    			AcNamedeb[dictKey] = 'IGST RECOVERY- FLEX'
                    			Narrationdeb[dictKey] ='UPI' + ' ' +  str(i)
                    			GLACcred[dictKey] = '208080261'
                    			AcNamecred[dictKey] = 'GST LIABILITY- Flex'
                    			Narrationcred[dictKey] ='UPI' + ' ' +  str(i)
		    if i[0:3]=='Ben':
			if  i[-3:]=='Fee' in i  and 'Switching Fee' not in i :
				dictKey=i.split(' ')[0]+' '+i.split(' ')[1]+' '+i.split(' ')[-3]+' '+i.split(' ')[-1]
               		        benfee = i.split(' ')[1] + ' ' + i.split(' ')[-3] + ' ' + i.split(' ')[-1]	
				if dictKey not in dict1.keys():
					dict1[dictKey]=[]
                    			dict1[dictKey].append(str(i))
                    			GLACdeb[dictKey]='404210037'
                    			AcNamedeb[dictKey]='UPI expense A/c'
                   		        Narrationdeb[dictKey]='UPI' + ' ' + str(i)
                    			GLACcred[dictKey]='302250016'
                    			AcNamecred[dictKey]='UPI INCOME A/C'
                    			Narrationcred[dictKey]='UPI'+' '+str(i)
			if i[-7:]=='Fee GST' in i and  'Switching Fee GST' not in i:
				dictKey=i.split(' ')[0]+' '+i.split(' ')[1]+' '+i.split(' ')[2]+' '+i.split(' ')[-2]+' '+i.split(' ')[-1]
		                bengst = i.split(' ')[1] + ' ' + i.split(' ')[2] + ' ' + i.split(' ')[-2] + ' ' + i.split(' ')[-1]
				if dictKey not in dict1.keys():
					dict1[dictKey] = []
                    			dict1[dictKey].append(str(i))
                    			GLACdeb[dictKey] = '114070217'
                    			AcNamedeb[dictKey] = 'IGST RECOVERY- FLEX'
                    			Narrationdeb[dictKey] ='UPI' + ' ' +  str(i)
                    			GLACcred[dictKey] = '208080261'
                    			AcNamecred[dictKey] = 'GST LIABILITY- Flex'
                    			Narrationcred[dictKey] = 'UPI'+' '+str(i)
			if 'Switching Fee' in i and 'Switching Fee GST' not in i:
				dictKey=i.split(' ')[0]+''+i.split(' ')[1]+' '+i.split(' ')[2]+' '+i.split(' ')[-2]+' '+i.split(' ')[-1]
		                benswitchfee = i.split(' ')[1] + ' ' + i.split(' ')[2] + ' ' + i.split(' ')[-1]
				if benfee == benswitchfee:
					for key, value in dict1.items():
						if switchfee in key and gst not in key and 'Remitter' not in key:
							value.append(i)
                            				GLACdeb[dictKey] = '404210037'
                            				AcNamedeb[dictKey] = 'UPI expense A/c'
                            				Narrationdeb[dictKey] ='UPI' + ' ' +  str(i)
                            				GLACcred[dictKey] = '302250016'
                            				AcNamecred[dictKey] = 'UPI INCOME A/C'
                            				Narrationcred[dictKey] ='UPI' + ' ' +  str(i)
				else:
					dictKey not in dict1.keys()
                    			dict1[dictKey]=[]
                    			dict1[dictKey].append(str(i))
                    			GLACdeb[dictKey]='404210037'
                    			AcNamedeb[dictKey]='UPI expense A/c'
                    			Narrationdeb[dictKey]='UPI' + ' ' + str(i)
                    			GLACcred[dictKey]='302250016'
                    			AcNamecred[dictKey]='UPI INCOME A/C'
                    			Narrationcred[dictKey]='UPI' + ' ' + str(i)
			if  'Switching Fee GST' in i:
				dictKey = i.split(' ')[0] + ' ' + i.split(' ')[1] + ' ' + i.split(' ')[2] + ' ' + i.split(' ')[-3]+ ' ' + i.split(' ')[-2] + ' ' + i.split(' ')[-1]
                		bengstfee = i.split(' ')[1] + ' ' + i.split(' ')[2] + ' ' + i.split(' ')[-2] + ' ' + i.split(' ')[-1]
				if bengst == bengstfee:
					for key, value in dict1.items():
						if bengstfee in key and 'Remitter' not in key:
							value.append(i)
                            				GLACdeb[dictKey] = '114070217'
                            				AcNamedeb[dictKey] = 'IGST RECOVERY- FLEX'
                            				Narrationdeb[dictKey] ='UPI' + ' ' +  str(i)
                            				GLACcred[dictKey] = '208080261'
                            				AcNamecred[dictKey] = 'GST LIABILITY- Flex'
                            				Narrationcred[dictKey] = 'UPI' + ' ' + str(i)
				else:
					dictKey not in dict1.keys()
                    			dict1[dictKey] = []
                    			dict1[dictKey].append(str(i))
                    			GLACdeb[dictKey] = '114070217'
                    			AcNamedeb[dictKey] = 'IGST RECOVERY- FLEX'
                    			Narrationdeb[dictKey] = 'UPI' + ' ' + str(i)
                    			GLACcred[dictKey] = '208080261'
                    			AcNamecred[dictKey] = 'UPI INWARD ACCOUNT'
                    			Narrationcred[dictKey] = 'UPI' + ' ' + str(i)
			if  'Transaction Amount' in i:
				dictKey=i.split(' ')[0]+' '+i.split(' ')[1]+' '+i.split(' ')[2]+' '+i.split(' ')[-2]+' '+i.split(' ')[-1]
				if dictKey not in dict1.keys():
					dict1[dictKey] = []
                			dict1[dictKey].append(str(i))
                			GLACdeb[dictKey] = '200000120275'
                			AcNamedeb[dictKey] = 'UPI OUTWARD ACCOUNT'
                			Narrationdeb[dictKey] ='UPI' + ' ' +  str(i)
                			GLACcred[dictKey] = '200000120288'
                			AcNamecred[dictKey] = 'UPI INWARD ACCOUNT'
                			Narrationcred[dictKey] = 'UPI' + ' ' + str(i)
		    if i[0:3]=='Rem':
			if  i[-3:]=='Fee' in i and 'Switching Fee' not in i :
				dictKey=i.split(' ')[0]+' '+i.split(' ')[1]+' '+i.split(' ')[-3]+' '+i.split(' ')[-1]
                		fee=i.split(' ')[1]+' '+i.split(' ')[-3]+' '+i.split(' ')[-1]
				if dictKey not in dict1.keys():
					dict1[dictKey]=[]
                    			dict1[dictKey].append(str(i))
                    			GLACdeb[dictKey]='404210037'
                    			AcNamedeb[dictKey]='UPI expense A/c'
                    			Narrationdeb[dictKey]='UPI' + ' ' + str(i)
                    			GLACcred[dictKey]='302250016'
                    			AcNamecred[dictKey]='UPI INCOME A/C'
                    			Narrationcred[dictKey]='UPI'+' '+str(i)
			if i[-7:]=='Fee GST' in i and  'Switching Fee GST' not in i:
				dictKey=i.split(' ')[0]+' '+i.split(' ')[1]+' '+i.split(' ')[2]+' '+i.split(' ')[-2]+' '+i.split(' ')[-1]
                		gst=i.split(' ')[1]+' '+i.split(' ')[2]+' '+i.split(' ')[-2]+' '+i.split(' ')[-1]
				if dictKey not in dict1.keys():
					dict1[dictKey] = []
                    			dict1[dictKey].append(str(i))
                    			GLACdeb[dictKey] = '114070217'
                    			AcNamedeb[dictKey] = 'IGST RECOVERY- FLEX'
                    			Narrationdeb[dictKey] ='UPI' + ' ' +  str(i)
                    			GLACcred[dictKey] = '208080261'
                    			AcNamecred[dictKey] = 'GST LIABILITY- Flex'
                    			Narrationcred[dictKey] = 'UPI'+' '+str(i)
			if 'Switching Fee' in i and 'Switching Fee GST' not in i:
				dictKey=i.split(' ')[0]+' '+i.split(' ')[1]+' '+i.split(' ')[2]+' '+i.split(' ')[-2]+' '+i.split(' ')[-1]
                		switchfee=i.split(' ')[1]+' '+i.split(' ')[2]+' '+i.split(' ')[-1]
				if fee==switchfee:
					for key,value in dict1.items():
						if switchfee in key and gst not in key and 'Beneficiary' not in value:
							value.append(i)
                           			 	GLACdeb[dictKey] = '404210037'
                            				AcNamedeb[dictKey] = 'UPI expense A/c'
                            				Narrationdeb[dictKey] ='UPI' + ' ' +  str(i)
                            				GLACcred[dictKey] = '302250016'
                            				AcNamecred[dictKey] = 'UPI INCOME A/C'
                            				Narrationcred[dictKey] ='UPI' + ' ' +  str(i)
				else:
					dictKey not in dict1.keys()
					dict1[dictKey]=[]
                    			dict1[dictKey].append(str(i))
                    			GLACdeb[dictKey]='404210037'
                    			AcNamedeb[dictKey]='UPI expense A/c'
                    			Narrationdeb[dictKey]='UPI' + ' ' + str(i)
                    			GLACcred[dictKey]='302250016'
                    			AcNamecred[dictKey]='UPI INCOME A/C'
                    			Narrationcred[dictKey]='UPI'+' '+str(i)
			if  'Switching Fee GST' in i:
				dictKey = i.split(' ')[0] + ' ' + i.split(' ')[1] + ' ' + i.split(' ')[2] + ' ' + i.split(' ')[-3]+ ' ' + i.split(' ')[-2] + ' ' + i.split(' ')[-1]
                		gstfee=i.split(' ')[1] + ' ' + i.split(' ')[2]+' '+i.split(' ')[-2]+' '+i.split(' ')[-1]
				if gst==gstfee:
					for key,value in dict1.items():
						if gstfee in key and 'Beneficiary' not in value:
							value.append(i)
                            				GLACdeb[dictKey] = '114070217'
                            				AcNamedeb[dictKey] = 'IGST RECOVERY- FLEX'
                            				Narrationdeb[dictKey] ='UPI' + ' ' +  str(i)
                            				GLACcred[dictKey] = '208080261'
                            				AcNamecred[dictKey] = 'GST LIABILITY- Flex'
                            				Narrationcred[dictKey] = 'UPI' + ' ' + str(i)
				else:
					dictKey not in dict1.keys()
                    			dict1[dictKey] = []
                    			dict1[dictKey].append(str(i))
                    			GLACdeb[dictKey] = '114070217'
                    			AcNamedeb[dictKey] = 'IGST RECOVERY- FLEX'
                    			Narrationdeb[dictKey] ='UPI' + ' ' +  str(i)
                    			GLACcred[dictKey] = '208080261'
                    			AcNamecred[dictKey] = 'GST LIABILITY- Flex'
                    			Narrationcred[dictKey] = 'UPI'+' '+str(i)
			if  'Transaction Amount' in i:
				dictKey=i.split(' ')[0]+' '+i.split(' ')[1]+' '+i.split(' ')[2]+' '+i.split(' ')[-2]+' '+i.split(' ')[-1]
                		if dictKey not in dict1.keys():
					dict1[dictKey] = []
                    			dict1[dictKey].append(str(i))
                    			GLACdeb[dictKey] = '200000120275'
                    			AcNamedeb[dictKey] = 'UPI OUTWARD ACCOUNT'
                    			Narrationdeb[dictKey] ='UPI' + ' ' +  str(i)
                    			GLACcred[dictKey] = '200000120288'
                    			AcNamecred[dictKey] = 'UPI INWARD ACCOUNT'
                    			Narrationcred[dictKey] = str(i)


            for i in dict1:
                sample = pandas.DataFrame()
                for j in dict1[i]:
		   if i == 'Final Settlement Amount' or i == 'Net Adjusted Amount' or i == 'Net Adjusted Fee with Tax':
                	sample=sample.append(df[df['Description'] == j])
			if i == 'Net Adjusted Amount':
                   		sample= sample.drop_duplicates(keep='first')
			
		   elif 'Approved' in j:
                       sample = sample.append(df[df['Description'] == j])
                dbs = []
                debit = []
                credit = []
                des = []
                for inn, row in sample.iterrows():
                    des.append(row['Description'])
		    if row['Description']=='Final Settlement Amount':
                  	if row['Debit'] > 0:
                      		credit.append(row['Debit'])
                  	if row['Credit'] > 0:
                      		debit.append(row['Credit'])
                    elif row['Debit'] > 0:
                        	debit.append(row['Debit'])
                    elif row['Credit'] > 0:
                        	credit.append(row['Credit'])

                if len(debit) > 1:

                    sample1 = pandas.DataFrame()

                    dsum = sum(debit)
                    sample1['Dr'] = [dsum]
                    sample1['GL AC'] = [GLACdeb[i]]
                    sample1['Ac Name'] = [AcNamedeb[i]]
                    sample1['Narration'] = Narrationdeb[i] + '-' + cycle + dt + date
                    maindf = maindf.append(sample1)

                elif len(credit) > 1:
                    sample2 = pandas.DataFrame()
                    dsum = sum(credit)
                    sample2['Cr'] = [dsum]
                    sample2['GL AC'] = [GLACcred[i]]
                    sample2['Ac Name'] = [AcNamecred[i]]
                    sample2['Narration'] = Narrationcred[i] + '-' + '-' + cycle + dt + date
                    maindf = maindf.append(sample2)
                elif len(credit) == 1 and len(debit) == 1:
                    sample2 = pandas.DataFrame()
                    if row['Description'] == 'Beneficiary/Remitter Sub Totals':
                        if debit > credit:
                            sample2['Cr'] = [debit[0] - credit[0]]
                            sample2['GL AC'] = [GLACdeb[i]]
                            sample2['Ac Name'] = [AcNamedeb[i]]
                            sample2['Narration'] = Narrationdeb[i] + '-' + cycle + dt + date
                            maindf = maindf.append(sample2)
                        if debit < credit:
                            sample2['Cr'] = [credit[0] - debit[0]]
                            sample2['GL AC'] = [GLACdeb[i]]
                            sample2['Ac Name'] = [AcNamedeb[i]]
                            sample2['Narration'] = Narrationdeb[i] + '-' + cycle + dt + date
                            maindf = maindf.append(sample2)
                    if row['Description'] != 'Beneficiary/Remitter Sub Totals':
                        sample2['Dr'] = debit
                        sample2['GL AC'] = [GLACdeb[i]]
                        sample2['Ac Name'] = [AcNamedeb[i]]
                        if row['Description'] not in des[0]:
                            if row['Description'] in ['Beneficiary U2 Approved NPCI Switching Fee',
                                                      'Beneficiary U2 Approved NPCI Switching Fee GST',
                                                      'Beneficiary Fin-BBPS U2 Approved NPCI Switching Fee',
                                                      'Beneficiary Fin-BBPS U2 Approved NPCI Switching Fee GST',
                                                      'Beneficiary SOD U2 Approved NPCI Switching Fee',
                                                      'Beneficiary SOD U2 Approved NPCI Switching Fee GST',
                                                      'Beneficiary SOD U2-RB Approved NPCI Switching Fee',
                                                      'Beneficiary SOD U2-RB Approved NPCI Switching Fee GST']:
                                sample2['Narration'] = Narrationcredben[i] + '-' + cycle + dt + date
			    else:
			
                           	  sample2['Narration']= 'UPI'+' '+row['Description']+'-'+cycle+dt+date
                        else:
                            sample2['Narration'] = Narrationdeb[i] + '-' + cycle + dt + date
                        maindf = maindf.append(sample2)
                        sample2 = pandas.DataFrame()
                        sample2['Cr'] = [credit[0]]
                        sample2['GL AC'] = [GLACcred[i]]
                        sample2['Ac Name'] = [AcNamecred[i]]
                        if row['Description'] in des[0]:
                            if row['Description'] in ['Beneficiary U2 Approved NPCI Switching Fee GST',
                                                      'Beneficiary Fin-BBPS U2 Approved NPCI Switching Fee',
                                                      'Beneficiary Fin-BBPS U2 Approved NPCI Switching Fee GST',
                                                      'Beneficiary SOD U2 Approved NPCI Switching Fee',
                                                      'Beneficiary SOD U2 Approved NPCI Switching Fee GST',
                                                      'Beneficiary SOD U2-RB Approved NPCI Switching Fee',
                                                      'Beneficiary SOD U2-RB Approved NPCI Switching Fee GST']:
                                sample2['Narration'] = Narrationcredben[i] + '-' + cycle + dt + date
			    else:
				                   
                            	sample2['Narration']= 'UPI'+' '+row['Description']+'-'+cycle+dt+date
                        else:
                            sample2['Narration'] = Narrationcred[i] + '-' + cycle + dt + date
                        maindf = maindf.append(sample2)

                elif len(debit) == 1 and len(credit) == 0:

                    sample3 = pandas.DataFrame()
                    sample3['Dr'] = debit
                    sample3['GL AC'] = [GLACdeb[i]]
                    sample3['Ac Name'] = [AcNamedeb[i]]
                    sample3['Narration'] = Narrationdeb[i] + '-' + cycle + dt + date
                    maindf = maindf.append(sample3)

                elif len(debit) == 0 and len(credit) == 1:
                    sample4 = pandas.DataFrame()
                    sample4['Cr'] = [credit[0]]
                    sample4['GL AC'] = [GLACcred[i]]
                    sample4['Ac Name'] = [AcNamecred[i]]
                    sample4['Narration'] = Narrationcred[i] + '-' + cycle + dt + date

                    maindf = maindf.append(sample4)


            
	            
	    if cycle == '1C':
                df1C = maindf.copy()
		df1C=df1C.reset_index()
			
		df11C = pandas.DataFrame()
		df1C['Narration']=df1C['Narration'].str.replace(' ', '')
	        netamt = df1C[df1C['Narration'] == 'UPINetAdjustedAmount-1C-DT-'+date]
	        nettax = df1C[df1C['Narration'] == 'UPINetAdjustedFeewithTax-1C-DT-'+date]

	        df1C.drop(df1C[df1C['Narration'] == 'UPINetAdjustedAmount-1C-DT-'+date].index, inplace=True)
	        df1C.drop(df1C[df1C['Narration'] == 'UPINetAdjustedFeewithTax-1C-DT-'+date].index, inplace=True)	
		
		df1C = df1C.groupby(['GL AC', 'Ac Name'], as_index=False)['Cr', 'Dr'].sum()
		
        	exp = df1C[df1C['GL AC'] == '404210037']
        	igst = df1C[df1C['GL AC'] == '114070217']
        	income = df1C[df1C['GL AC'] == '302250016']
        	gst1 = df1C[df1C['GL AC'] == '208080261']
        	rtgs = df1C[df1C['GL AC'] == '110040003']
        	inward = df1C[df1C['GL AC'] == '200000120288']
        	outward = df1C[df1C['GL AC'] == '200000120275']
        	df11C = df11C.append([exp, igst, income, gst1, rtgs, inward, outward], ignore_index=True)
	
		df11C['Narration'] = ['UPI Approved Fee-1C-DT-' + date, 'UPI Approved Fee IGST-1C-DT- ' + date,
                              'UPI Approved Fee-1C-DT- ' + date, 'UPI Approved Fee GST-1C-DT- ' + date,
                              'UPI Final Settlement-1C-DT- ' + date, 'UPI Approved Txn Amt-1C-DT- ' + date,
                              'UPI Approved Txn Amt-1C-DT- ' + date]
        	df11C = df11C.append([netamt, nettax], ignore_index=True)

                df11C = df11C.fillna('0')
       
        	upi.append('UPI_NTSLEQT_1C')
		print len(df11C)

        	C1 = True
            if cycle == '2C':
                df2C = maindf.copy()
		df2C=df2C.reset_index()
        	df2C.drop(df2C[df2C['Narration'] == 'UPI Net Adjusted Amount-2C-DT-' + date].index, inplace=True)
        	df2C.drop(df2C[df2C['Narration'] == 'UPI Net Adjusted Fee with Tax-2C-DT-' + date].index, inplace=True)
        	df22C = pandas.DataFrame()
		df2C = df2C.groupby(['GL AC', 'Ac Name'], as_index=False)['Cr', 'Dr'].sum()

        	exp = df2C[df2C['GL AC'] == '404210037']
        	igst = df2C[df2C['GL AC'] == '114070217']
        	income = df2C[df2C['GL AC'] == '302250016']
        	gst1 = df2C[df2C['GL AC'] == '208080261']
        	rtgs = df2C[df2C['GL AC'] == '110040003']
        	inward = df2C[df2C['GL AC'] == '200000120288']
        	outward = df2C[df2C['GL AC'] == '200000120275']
        	df22C = df22C.append([exp, igst, income, gst1, rtgs, inward, outward], ignore_index=True)
        
        	df22C['Narration'] = ['UPI Approved Fee-2C-DT-' + date, 'UPI Approved Fee IGST-2C-DT- ' + date,
                              'UPI Approved Fee-2C-DT- ' + date, 'UPI Approved Fee GST-2C-DT- ' + date,
                              'UPI Final Settlement-2C-DT- ' + date, 'UPI Approved Txn Amt-2C-DT- ' + date,
                              'UPI Approved Txn Amt-2C-DT- ' + date]

        	df22C = df22C.fillna('0')
        
        	upi.append('UPI_NTSLEQT_2C')
		print len(df22C)

        	C2 = True

                
            if cycle == '3C':
                df3C = maindf.copy()
		df3C=df3C.reset_index()
		df3C.drop(df3C[df3C['Narration'] == 'UPI Net Adjusted Amount-3C-DT-' + date].index, inplace=True)
        	df3C.drop(df3C[df3C['Narration'] == 'UPI Net Adjusted Fee with Tax-3C-DT-' + date].index, inplace=True)
        	df33C = pandas.DataFrame()
        	df3C = df3C.groupby(['GL AC', 'Ac Name'], as_index=False)['Cr', 'Dr'].sum()

        	exp = df3C[df3C['GL AC'] == '404210037']
        	igst = df3C[df3C['GL AC'] == '114070217']
        	income = df3C[df3C['GL AC'] == '302250016']
       		gst1 = df3C[df3C['GL AC'] == '208080261']
        	rtgs = df3C[df3C['GL AC'] == '110040003']
        	inward = df3C[df3C['GL AC'] == '200000120288']
        	outward = df3C[df3C['GL AC'] == '200000120275']
        	df33C = df33C.append([exp, igst, income, gst1, rtgs, inward, outward], ignore_index=True)
       
        	df33C['Narration'] = ['UPI Approved Fee-3C-DT-' + date, 'UPI Approved Fee IGST-3C-DT- ' + date,
                              'UPI Approved Fee-3C-DT- ' + date, 'UPI Approved Fee GST-3C-DT- ' + date,
                              'UPI Final Settlement-3C-DT- ' + date, 'UPI Approved Txn Amt-3C-DT- ' + date,
                              'UPI Approved Txn Amt-3C-DT- ' + date]
		df33C = df33C.fillna('0')
       		
        	upi.append('UPI_NTSLEQT_3C')

        	print len(df33C)
        	C3 = True
            if cycle == '4C':
                df4C = maindf.copy()
		df4C=df4C.reset_index()
		df4C.drop(df4C[df4C['Narration'] == 'UPI Net Adjusted Amount-4C-DT-' + date].index, inplace=True)
       		df4C.drop(df4C[df4C['Narration'] == 'UPI Net Adjusted Fee with Tax-4C-DT-' + date].index, inplace=True)
        	df44C = pandas.DataFrame()
        	df4C = df4C.groupby(['GL AC', 'Ac Name'], as_index=False)['Cr', 'Dr'].sum()

        	exp = df4C[df4C['GL AC'] == '404210037']
        	igst = df4C[df4C['GL AC'] == '114070217']
        	income = df4C[df4C['GL AC'] == '302250016']
        	gst1 = df4C[df4C['GL AC'] == '208080261']
        	rtgs = df4C[df4C['GL AC'] == '110040003']
        	inward = df4C[df4C['GL AC'] == '200000120288']
        	outward = df4C[df4C['GL AC'] == '200000120275']
        	df44C = df44C.append([exp, igst, income, gst1, rtgs, inward, outward], ignore_index=True)
        
        	df44C['Narration'] = ['UPI Approved Fee-4C-DT-' + date, 'UPI Approved Fee IGST4C-DT- ' + date,
                              'UPI Approved Fee-4C-DT- ' + date, 'UPI Approved Fee GST-4C-DT- ' + date,
                              'UPI Final Settlement-4C-DT- ' + date, 'UPI Approved Txn Amt-4C-DT- ' + date,
                              'UPI Approved Txn Amt-4C-DT- ' + date]
		df44C = df44C.fillna('0')
	       
        	upi.append('UPI_NTSLEQT_4C')

        	print len(df44C)
        	C4 = True


        dfs = {}
        #imps = ['UPI_NTSLEQT_1C', 'UPI_NTSLEQT_2C', 'UPI_NTSLEQT_3C', 'UPI_NTSLEQT_4C']
        dfslist = []
        if C1:
            dfslist.append(df11C)
        if C2:
            dfslist.append(df22C)
        if C3:
            dfslist.append(df33C)
        if C4:
            dfslist.append(df44C)

        for i, j in zip(upi, dfslist):
            if len(j) > 0:
                dfs[i] = j

        if not os.path.exists(dest + '/' + 'OUTPUT'):
            os.mkdir(dest + '/' + 'OUTPUT')
        destpath = dest + '/' + 'OUTPUT/'
        rmpath = destpath + '*'
        rmfiles = glob.glob(rmpath)
        for i in rmfiles:
            os.remove(i)

        for i in dfs.keys():
            print i

            count = 1

            dfs[i].to_csv(destpath + i + '.csv', index=False)
            count += 1
        newPath = newPath + query['fname'].split('_')[0] + '_' + 'REPORT' + '/' + date + '/' + 'OUTPUT/'

        if os.path.exists(newPath):

            shutil.make_archive('UPI', 'zip', newPath)

            if os.path.exists('/usr/share/nginx/www/ngerecon/ui/files/Outputs/UPI.zip'):
                os.remove('/usr/share/nginx/www/ngerecon/ui/files/Outputs/UPI.zip')
            shutil.move('UPI.zip', '/usr/share/nginx/www/ngerecon/ui/files/Outputs/')
            fpath = '/files/Outputs/' + 'UPI.zip'
            print fpath
            return True, fpath
        else:
            return False, 'No FIle Found'
