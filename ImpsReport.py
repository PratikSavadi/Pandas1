import pandas
import os
import shutil
import datetime
import zipfile
import re
import glob
class GenerateReport():
    def __init__(self):
        pass

    def getImpsReport(self,query):
	print 'alare'
	print query
	date= query['date']
	print date
	
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
            print(query['path'] + query['fname'])
            print( newPath + query['fname'].split('_')[0] + '_' + 'REPORT' + '/' + query['date'])
	    
            shutil.copy(query['path'] + query['fname'],
                        newPath + query['fname'].split('_')[0] + '_' + 'REPORT' + '/' + query['date'])
	readPath = newPath + query['fname'].split('_')[0] + '_' + 'REPORT' + '/' + query['date']
	print readPath
        # reqDate = str(datetime.date.today())

        path = readPath + '/' + query['fname']
        dest = readPath
        
       
        with zipfile.ZipFile(path, 'r') as zf:
            listOfFileNames = zf.namelist()
            print(listOfFileNames)

            for fileName in listOfFileNames:
                if fileName.endswith('.xlsx'):
		
                    zf.extract(fileName, dest)
        reqDate = listOfFileNames[0].split('_')[0][-6:].strip()
	
        if os.path.exists(dest):
	    filelist=[]
            files = os.listdir(dest)
	    for i in files:
		if i.startswith('IMPSNTSLEQT'): 
		     filelist.append(i)
	    
            file = [i for i in filelist if re.match('[A-Z]{11}[0-9]{6}_[0-9]{1}C', i)]
	    
        else:
            print("no execution found")
        # df2=pd.DataFrame()
        # files = ['IMPSNTSLEQT010919_1C.xlsx']
	C1=False
        C2=False
        C3=False
        C4=False

        for a in file:
	    print a
            df = pandas.read_excel(dest + '/' + a, skiprows=4)
	    
            df["cycle"] = a.split('.')[0].split('_')[-1]
            cycle = df["cycle"].unique()
            df2 = df[df['Description'].isin(['Remitter P2A Approved Fee', 'Remitter P2A Approved NPCI Switching Fee'])]
            if len(df2):
                df_feeRem = df2.copy()
                df_feeRem['Remarks'] = 'Fee'
                df_feeRem = df_feeRem.groupby(['Remarks'], as_index=False)['Debit'].sum()
                df_feeRem.rename(columns={'Debit': 'Dr'}, inplace=True)
                df_feeRem = df_feeRem.assign(
                    **{'Narration': 'IMPS REM P2A APP Fee-' + df["cycle"] + '-DT' + reqDate, 'Cr': 0,
                       'Ac Name': 'IMPS EXPENSES',
                       'GL AC': '404210010'})
            else:
                df_feeRem = pandas.DataFrame()

            df2 = df[df['Description'].isin(
                ['Remitter P2A Approved Fee GST', 'Remitter P2A Approved NPCI Switching Fee GST'])]
            if len(df2):
                df_feegstRem = df2.copy()
                df_feegstRem['Remarks'] = 'Fee'
                df_feegstRem = df_feegstRem.groupby(['Remarks'], as_index=False)['Debit'].sum()
                df_feegstRem.rename(columns={'Debit': 'Dr'}, inplace=True)
                df_feegstRem = df_feegstRem.assign(
                    **{'Narration': 'IMPS REM P2A APP Fee IGST-' + df["cycle"] + '-DT' + reqDate, 'Cr': 0,
                       'Ac Name': 'IGST RECOVERY -  Flex',
                       'GL AC': '114070217'})
            else:
                df_feegstRem = pandas.DataFrame()

            df2 = df[df['Description'].isin(['Remitter P2A Approved Transaction Amount'])]
            if len(df2):
                df_sumRem = df2.copy()
                df_sumRem = df_sumRem.assign(
                    **{'Narration': 'IMPS REM P2A APP Txn Amt-' + df["cycle"] + '-DT' + reqDate, 'Cr': 0,
                       'Ac Name': 'IMPS Outward Settlement A/c',
                       'GL AC': '200000508888'})
                df_sumRem.rename(columns={'Debit': 'Dr'}, inplace=True)
                df_sumRem.drop(['Description', 'No of Txns', 'Credit'], inplace=True, axis=1)
            else:
                df_sumRem = pandas.DataFrame()

            df2 = df[
                df['Description'].isin(['Remitter P2A-08 Approved Fee', 'Remitter P2A-08 Approved NPCI Switching Fee'])]
            if len(df2):
                df_feeP208Rem = df2.copy()
                df_feeP208Rem['Remarks'] = 'Fee'
                df_feeP208Rem = df_feeP208Rem.groupby(['Remarks'], as_index=False)['Debit'].sum()
                df_feeP208Rem.rename(columns={'Debit': 'Dr'}, inplace=True)
                df_feeP208Rem = df_feeP208Rem.assign(
                    **{'Narration': 'IMPS REM P208 APP Fee-' + df["cycle"] + '-DT' + reqDate, 'Cr': 0,
                       'Ac Name': 'IMPS EXPENSES',
                       'GL AC': '404210010'})
            else:
                df_feeP208Rem = pandas.DataFrame()

            df2 = df[df['Description'].isin(
                ['Remitter P2A-08 Approved Fee GST', 'Remitter P2A-08 Approved NPCI Switching Fee GST'])]
            if len(df2):
                df_feegstP208Rem = df2.copy()
                df_feegstP208Rem['Remarks'] = 'Fee'
                df_feegstP208Rem = df_feegstP208Rem.groupby(['Remarks'], as_index=False)['Debit'].sum()
                df_feegstP208Rem.rename(columns={'Debit': 'Dr'}, inplace=True)
                df_feegstP208Rem = df_feegstP208Rem.assign(
                    **{'Narration': 'IMPS Remitter P2A-08 APP Fee IGST-' + df["cycle"] + '-DT' + reqDate, 'Cr': 0,
                       'Ac Name': 'IGST RECOVERY -  Flex',
                       'GL AC': '114070217'})
            else:
                df_feegstP208Rem = pandas.DataFrame()

            df2 = df[df['Description'].isin(['Remitter P2A-08 Approved Transaction Amount'])]
            if len(df2):
                df_sumP208Rem = df2.copy()
                df_sumP208Rem = df_sumP208Rem.assign(
                    **{'Narration': 'IMPS REM P2A APP Txn Amt-' + df["cycle"] + '-DT' + reqDate, 'Cr': 0,
                       'Ac Name': 'IMPS Outward Settlement A/c',
                       'GL AC': '200000508888'})
                df_sumP208Rem.rename(columns={'Debit': 'Dr'}, inplace=True)
                df_sumP208Rem.drop(['Description', 'No of Txns', 'Credit'], inplace=True, axis=1)
            else:
                df_sumP208Rem = pandas.DataFrame()

            df2 = df[df['Description'].isin(['Beneficiary MRT Approved Fee'])]
            if len(df2):
                df_feeBenf = df2.copy()
                df_feeBenf = df_feeBenf.assign(
                    **{'Narration': 'IMPS BEN MRT APP Fee-' + df["cycle"] + '-DT' + reqDate, 'Dr': 0,
                       'Ac Name': 'IMPS INCOME',
                       'GL AC': '302210201'})
                df_feeBenf.rename(columns={'Credit': 'Cr'}, inplace=True)
                df_feeBenf.drop(['Description', 'No of Txns', 'Debit'], inplace=True, axis=1)
            else:
                df_feeBenf = pandas.DataFrame()

            df2 = df[df['Description'].isin(['Beneficiary MRT Approved Fee GST'])]
            if len(df2):
                df_feegstBenf = df2.copy()
                df_feegstBenf = df_feegstBenf.assign(
                    **{'Narration': 'IMPS BEN MRT APP Fee GST-' + df["cycle"] + '-DT' + reqDate, 'Dr': 0,
                       'Ac Name': 'GST LIABILITY- Flex',
                       'GL AC': '208080261'})
                df_feegstBenf.rename(columns={'Credit': 'Cr'}, inplace=True)
                df_feegstBenf.drop(['Description', 'No of Txns', 'Debit'], inplace=True, axis=1)
            else:
                df_feegstBenf = pandas.DataFrame()

            df2 = df[df['Description'].isin(['Beneficiary MRT Approved Transaction Amount'])]
            if len(df2):
                df_sumBenf = df2.copy()
                df_sumBenf = df_sumBenf.assign(
                    **{'Narration': 'IMPS BEN MRT APP Txn Amt-' + df["cycle"] + '-DT' + reqDate, 'Dr': 0,
                       'Ac Name': 'IMPS Inward Settlement A/c',
                       'GL AC': '200000508890'})
                df_sumBenf.rename(columns={'Credit': 'Cr'}, inplace=True)
                df_sumBenf.drop(['Description', 'No of Txns', 'Debit'], inplace=True, axis=1)
            else:
                df_sumBenf = pandas.DataFrame()

            df2 = df[df['Description'].isin(['Beneficiary P2A Approved Fee'])]
            if len(df2):
                df_feeP208Benf = df2.copy()
                df_feeP208Benf = df_feeP208Benf.assign(
                    **{'Narration': 'IMPS BEN P2A APP Fee-' + df["cycle"] + '-DT' + reqDate, 'Dr': 0,
                       'Ac Name': 'IMPS INCOME',
                       'GL AC': '302210201'})
                df_feeP208Benf.rename(columns={'Credit': 'Cr'}, inplace=True)
                df_feeP208Benf.drop(['Description', 'No of Txns', 'Debit'], inplace=True, axis=1)
            else:
                df_feeP208Benf = pandas.DataFrame()

            df2 = df[df['Description'].isin(['Beneficiary P2A Approved Fee GST'])]
            if len(df2):
                df_feegstP208Benf = df2.copy()
                df_feegstP208Benf = df_feegstP208Benf.assign(
                    **{'Narration': 'IMPS BEN P2A APP Fee GST-' + df["cycle"] + '-DT' + reqDate, 'Dr': 0,
                       'Ac Name': 'GST LIABILITY- Flex',
                       'GL AC': '208080261'})
                df_feegstP208Benf.rename(columns={'Credit': 'Cr'}, inplace=True)
                df_feegstP208Benf.drop(['Description', 'No of Txns', 'Debit'], inplace=True, axis=1)
            else:
                df_feegstP208Benf = pandas.DataFrame()

            df2 = df[df['Description'].isin(['Beneficiary P2A Approved Transaction Amount'])]
            if len(df2):
                df_sumP208Benf = df2.copy()
                df_sumP208Benf = df_sumP208Benf.assign(
                    **{'Narration': 'IMPS BEN P2A APP Txn Amt-' + df["cycle"] + '-DT' + reqDate, 'Dr': 0,
                       'Ac Name': 'IMPS Inward Settlement A/c',
                       'GL AC': '200000508890'})
                df_sumP208Benf.rename(columns={'Credit': 'Cr'}, inplace=True)
                df_sumP208Benf.drop(['Description', 'No of Txns', 'Debit'], inplace=True, axis=1)
            else:
                df_sumP208Benf = pandas.DataFrame()

            df2 = df[df['Description'] == 'Beneficiary/Remitter Sub Totals']
            if len(df2):
                df_settlAmt = df2.copy()
                df_settlAmt.loc[len(df_settlAmt), 'Description'] = 'Settlement Amount'

                #  Assuming Settlement Amount is havung one row in description.So we have taken value of 0th index of debit and credit,
                #  if cr > dr then dr-cr and result will be under cr column
                df_settlAmt.loc[df_settlAmt['Description'] == 'Settlement Amount', 'Cr'] = \
                    df_settlAmt.loc[df_settlAmt.index[0]]['Debit'] - df_settlAmt.loc[df_settlAmt.index[0]]['Credit'] if \
                        df_settlAmt.loc[df_settlAmt.index[0]]['Debit'] > df_settlAmt.loc[df_settlAmt.index[0]][
                            'Credit'] else '0'
                df_settlAmt.loc[df_settlAmt['Description'] == 'Settlement Amount', 'Dr'] = \
                    df_settlAmt.loc[df_settlAmt.index[0]]['Credit'] - df_settlAmt.loc[df_settlAmt.index[0]]['Debit'] if \
                        df_settlAmt.loc[df_settlAmt.index[0]]['Credit'] > df_settlAmt.loc[df_settlAmt.index[0]][
                            'Debit'] else '0'
                df_settlAmt = df_settlAmt.assign(
                    **{'Narration': 'IMPS Final settlement-' + df["cycle"] + '-DT' + reqDate,
                       'Ac Name': 'RTGS SETTLEMENT ACCOUNT WITH RBI',
                       'GL AC': '110040003'})
                df_settlAmt.drop(df_settlAmt.index[[0]], inplace=True)
                df_settlAmt.drop(['Description', 'No of Txns', 'Debit', 'Credit'], inplace=True, axis=1)
            else:
                df_settlAmt = pandas.DataFrame()

            dfnew = df_feeRem.append(
                [df_feegstRem, df_sumRem, df_feeP208Rem, df_feegstP208Rem, df_sumP208Rem, df_feeBenf, df_feegstBenf,
                 df_sumBenf, df_feeP208Benf,
                 df_feegstP208Benf, df_sumP208Benf, df_settlAmt]).reset_index(drop=True)
            del [df_feeRem, df_feegstRem, df_sumRem, df_feeP208Rem, df_feegstP208Rem, df_sumP208Rem, df_feeBenf,
                 df_feegstBenf, df_sumBenf, df_feeP208Benf,
                 df_feegstP208Benf, df_sumP208Benf, df_settlAmt]
           

            if cycle == '1C':
                df1C = dfnew.copy()
                df1C.drop(['Remarks'], inplace=True, axis=1)
                df1C = df1C[['GL AC', 'Ac Name', 'Dr', 'Cr', 'Narration']]
        	print len(df1C)
	
	   	C1=True
                
		
            elif cycle == '2C':
                df2C = dfnew.copy()
                df2C.drop(['Remarks'], inplace=True, axis=1)
                df2C = df2C[['GL AC', 'Ac Name', 'Dr', 'Cr', 'Narration']]
		print df2C
		C2=True

            elif cycle == '3C':
                df3C = dfnew.copy()
                df3C.drop(['Remarks'], inplace=True, axis=1)
                df3C = df3C[['GL AC', 'Ac Name', 'Dr', 'Cr', 'Narration']]
		print df3C
		C3=True

            elif cycle == '4C':
                df4C = dfnew.copy()
                df4C.drop(['Remarks'], inplace=True, axis=1)
                df4C = df4C[['GL AC', 'Ac Name', 'Dr', 'Cr', 'Narration']]
		print df4C
		C4=True
	
#        if not os.path.exists(dest + '/' + 'OUTPUT'):
#                os.mkdir(dest + '/' + 'OUTPUT')
#        destpath = dest + '/' + 'OUTPUT/'
#        dfs = {}	
#	if len(df1C):  
#             dfs['IMPSNTSLEQT_1C']= df1C
#	     for a in dfs:
#	            dfs[a].to_csv(destpath + i + '.csv', index=False)
		    #print dfs[a]            		
        
	   
 
#        if len(df2C):
#             dfs ['IMPSNTSLEQT_2C'] = df2C
            # for b in dfs:
#	            dfs[b].to_csv(destpath + i + '.csv', index=False)
#		    print dfs[b]
#        if len(df3C):
#                 dfs['IMPSNTSLEQT_3C'] =df3C
#                 for c in dfs:
#                     dfs[c].to_csv(destpath + i + '.csv', index=False)
#        if len(df4C):
#                dfs['IMPSNTSLEQT_4C'] =df4C
#        
#                for d in dfs:
#                     dfs[d].to_csv(destpath + i + '.csv', index=False)

#       dfs = {'IMPSNTSLEQT_1C': df1C, 'IMPSNTSLEQT_2C': df2C, 'IMPSNTSLEQT_3C': df3C, 'IMPSNTSLEQT_4C': df4C}
	dfs={}
        imps=['IMPSNTSLEQT_1C','IMPSNTSLEQT_2C','IMPSNTSLEQT_3C','IMPSNTSLEQT_4C']
	dfslist=[]
	if C1:
          print C1
	  dfslist.append(df1C)
	if C2:
	  print C2
	  dfslist.append(df2C)
	if C3:
	   print C3
	   dfslist.append(df3C)
	if C4:
	    print C4
	    dfslist.append(df4C)	

        
     
	for i,j  in zip(imps,dfslist):
		if len(j)>0:
		   dfs[i]=j
		
        if not os.path.exists(dest + '/' + 'OUTPUT'):
            os.mkdir(dest + '/' + 'OUTPUT')
        destpath = dest + '/' + 'OUTPUT/'
        rmpath = destpath+'*'
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

            shutil.make_archive('IMPS', 'zip', newPath) 
            
            if os.path.exists('/usr/share/nginx/www/ngerecon/ui/files/Outputs/IMPS.zip'):
              os.remove('/usr/share/nginx/www/ngerecon/ui/files/Outputs/IMPS.zip') 
            shutil.move('IMPS.zip', '/usr/share/nginx/www/ngerecon/ui/files/Outputs/')
            fpath = '/files/Outputs/' + 'IMPS.zip'
	    print fpath
            return True, fpath
        else:
            return  False, 'No FIle Found'
