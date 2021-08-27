import json

#取得路徑
import sys
##print(len(sys.argv))
if len(sys.argv) == 3:
    path1 = './runs/detect/' + sys.argv[1] + '/'
    path2 = './runs/detect/' + sys.argv[2] + '/'
    print('try to find report.json in ', path1)
    print('and reference the labels in ', path2)

#從原本的json生成文字組所需資料格式
with open(path1+'report.json','r',encoding='utf8') as report:#讀取原檔
    recognize = json.load(report)
print('-'*15 + 'file loaded' + '-'*15)

count = 0
for invoice in recognize['img']:
    if invoice['maintype'] == '增值税发票' or invoice['childtype'] == '火车发票' or invoice['childtype'] == '公路客运发票':
        file_name = path2 + 'labels/' + invoice['img'][:-4] + '.txt' #目前裁切圖片都是以jpg儲存，若將來有改，請更動此處
##        print(file_name)
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
