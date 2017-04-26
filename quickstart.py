#!/usr/bin/env python
#coding:utf-8
from __future__ import print_function
import httplib2
import os
import json
import gspread as g
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.service_account import ServiceAccountCredentials

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
        
    return credentials

def main(): #mainには入出力の関数のみにする。関数を分けて種類を分ける
	credentials = get_credentials()
	c = g.authorize(credentials)
	sht = c.open('test').sheet1	
	
	Id_list=sht.range(1,1,1,10) 
	Maker_cell=sht.range(2,sht.find('メーカー').col,sht.row_count,sht.find('メーカー').col)
	Model_cell=sht.range(2,sht.find('型番').col,sht.row_count,sht.find('型番').col)	
	Maker_list=[] 
	Model_list=[]
	tab={}

	
	#set(maker_list) 
	for i in range(len(Maker_cell)):
		Maker_list.append(Maker_cell[i].value)	
	Maker_list=list(set(Maker_list))
		
	#del ''
	for i in range(len(Model_cell)):
		if Model_cell[i].value == '':
			pass
		else:
			Model_list.append(Model_cell[i])

	row_len=len(Model_list)




	#{maker:model}  --request--> #{model:row}
	for i in Maker_list:
		if i not in tab:
			tab.update({i:[]})

	for i in tab:
		for j in range(row_len):
			if i == Maker_cell[j].value and Model_cell[j] not in tab:
				tab[i].append(Model_cell[j])  #stack
							 

	print(tab)
		
def get_first(fld): #初期のタブ
	for i in fld:
		return i,fld[i].value,fld[i].row_values
	

""" 
	1.python側の処理の流れを大まかに完成させる
	  MakerName:ModelName→ModelName:RowNum→return row_values(範囲限定)
	
	
	2.djangoでwebアプリケーション構築してみる

	
	
dict作成	
	#dictにkey登録
	for i in Maker_list:
		container[i]=[]

	#dictにitem登録 メーカーでヒットさせて行番号を登録
	for j in container:	
		for i in Maker_cell:	
			if i.value == j:
				container[j].append(i.row)

json関係	
	↑1機種づつ作りたい↑
	 			↓
		['種類':'PC', 'メーカー':'Dell', '型番':'センサーPC', '管理番号':'PC4-1', '箱有無':'無', '所在':'本社','備考':'', '使用開始':'2017/1/17', '使用終了':'2017/5/31', 使用者:'田中'],
・・・メーカーごとにアウトプット(js)の段階でスプレッドシートみたいにして、項目とidを合わせる		
				
	
※idをどうとるか
  idにその他情報をどうやって紐づけるか→idだけ拾うと情報がばらける
  getの方向しか考えられていない。postするときの連携はどうするのか
  =cell情報で行を取る？
	json作成


＜今後＞
変更履歴、デッドロックなど
ー共有メモリ？？
   予約確定時に再度問い合わせ？
  変更履歴のファイル？
  貸出ステータス構築
	
"""	

if __name__ == '__main__':
	main()