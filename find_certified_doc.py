import json, sys, argparse, os

#取得路徑
parser = argparse.ArgumentParser()
parser.add_argument('--path1', '--1', nargs=1, type=str, help='file name of the prediction of the receipts recognition')
parser.add_argument('--path2', '--2', nargs=1, type=str, help='file name of the prediction of the bar code/QR code recognition')
folders = vars(parser.parse_args())
path1 = './runs/detect/' + folders['path1'][0] + '/'
path2 = './runs/detect/' + folders['path2'][0] + '/'

#從原本的json生成文字組所需資料格式
try:
    with open(path1+'report.json','r',encoding='utf8') as report:#讀取原檔
        recognize = json.load(report)
    print('-'*15 + 'file loaded' + '-'*15)
except FileNotFoundError:
    sys.exit(path1 + 'report.json not found')


count = 0
img_lost = 0
enforce = False
remind = 1
for invoice in recognize['img']:
    #防呆
    if img_lost > remind and not enforce:
        print('There\'re over ' + str(remind) + ' images not found. ')
        print('Please check whether your second path (path2) is correct.')
        wrong_ans = True
        while wrong_ans:
            ans = input('continue this process[y]\n' +
                        'cancel this process [n]\n' +
                        'continue, and remind me again if there are more images not found[r]:')
            if ans == 'y':
                enforce = True
                print('.'*3 + 'continue this process')
                wrong_ans = False
            elif ans == 'n':
                print('-'*10 + 'process stopped' + '-'*10)
                print('Please run \"split_json.py\" again to rewind what \"find_certified_doc.py\" have done.')
                sys.exit('path2 may be the the wrong path')
            elif ans == 'r':
                print('Remind again if the amount of images not found is over...?')
                wrong_ans2 = True
                while wrong_ans2:
                    ans2 = input('(please enter an integer, or enter [b] to back to the last question)')
                    if ans2 == 'b':
                        wrong_ans2 = False
                    else:
                        try:
                            remind = int(ans2)
                            wrong_ans2 = False
                            wrong_ans = False
                        except ValueError:
                            pass
    #過濾證明文件
    if invoice['maintype'] == '增值税发票' or invoice['childtype'] == '火车发票' or invoice['childtype'] == '公路客运发票':
        file_name = path2 + 'labels/' + invoice['img'][:-4] + '.txt' #目前裁切圖片都是以jpg儲存，若將來有改，請更動此處
        print(file_name)
        if os.path.isfile(path2 + invoice['img'][:-4] + '.jpg'):
            print('>'*5 + 'checking ' + file_name[:-4] + '.jpg') #目前裁切圖片都是以jpg儲存，若將來有改，請更動此處
        else:
            print('\033[93m ' + 'Warning: '+ invoice['img'][:-4] + '.jpg' +' is lost' + ' \033[0m')
            img_lost += 1
            continue
        try:
            with open(file_name,'r') as label_file:
                if label_file.read() == '':
                    recognize['img'][recognize['img'].index(invoice)]['maintype'] = '其它'
                    recognize['img'][recognize['img'].index(invoice)]['childtype'] = '其它'
                    print('>'*5 + 'change label of ' + recognize['img'][recognize['img'].index(invoice)]['img'])
                    print(' '*5 + 'because of no characteristic found')
                    count += 1
        except FileNotFoundError:
            recognize['img'][recognize['img'].index(invoice)]['maintype'] = '其它'
            recognize['img'][recognize['img'].index(invoice)]['childtype'] = '其它'
            print('>'*5 + 'change label of ' + recognize['img'][recognize['img'].index(invoice)]['img'])
            print(' '*5 + 'because of label file not found')
            count += 1

print('-'*40)
print('there\'re ' + str(count) + ' labels were changed')

with open(path1+'report.json','w',encoding='utf8') as report:
    json.dump(recognize, report, ensure_ascii=False,indent=4)
