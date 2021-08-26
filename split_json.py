import json
#從原本的json生成文字組所需資料格式
with open('AllLabel.json','r') as allLabel:#讀取原檔
    recognize = json.load(allLabel)
print('-'*15 + 'file loaded' + '-'*15)

#生成公司所需格式，讀取原檔的code在最上面
#以下兩個關係到公司方的取名
translate = {
    "10_blue_train":"火车发票",
    "11_red_train":"火车发票",
    "12_normal_vat":"增值税发票",
    "13_airport":"飞机行程单",
    "14_quota_receipt":"定额发票",
    "16_machine":"通用机打发票",
    "17_taxi":"出租车发票",
    "18_bus":"公路客运发票",
    "19_toll_fee_sh":"车辆通行费",
    '20_toll_fee_machine':"车辆通行费",
    'other':'其它'
    }
print('-'*15 + 'check if the child type names meet requirements' + '-'*15)
print(json.dumps(translate,indent=4,ensure_ascii=False))
classify = {
    "10_blue_train":"交通发票",
    "11_red_train":"交通发票",
    "12_normal_vat":"增值税发票",
    "13_airport":"交通发票",
    "14_quota_receipt":"定额发票",
    "16_machine":"通用机打发票",
    "17_taxi":"交通发票",
    "18_bus":"交通发票",
    "19_toll_fee_sh":"交通发票",
    '20_toll_fee_machine':"交通发票",
    'other':'其它'
    }
print('-'*15 + 'check if the main type names meet requirements' + '-'*15)
print(json.dumps(classify,indent=4,ensure_ascii=False))

#開始生成公司方所需格式
report = {}
img = []
count = 0
for image in recognize.keys():
    if recognize[image]['class'] == {}:
        img.append({
            'oringinimg' : recognize[image]['name'],
            'img' : recognize[image]['name'],
            'maintype' : classify['other'],
            'childtype': translate['other'],
            'result' : ''
            })
        continue
    else:
        for invoice in recognize[image]['class'].keys():
            img_info = {
                'oringinimg' : recognize[image]['name'],
                'img' : recognize[image]['name'][:-4] + invoice.rjust(3,'0') + '.jpg', #因為裁切圖片那邊有統一是.jpg，將來要調整儲存格式的話要調整
                'maintype' : classify[recognize[image]['class'][invoice]['subclass_str']],
                'childtype': translate[recognize[image]['class'][invoice]['subclass_str']],
                'result' : ''
                }
            img.append(img_info)
            count += 1
report['total'] = count
report['img'] = img
print('-'*15 + 'finish transferring' + '-'*15)
#以下另存為json檔，以上為dict
with open('report.json','w', encoding='utf8') as report_file:
    split_info_json = json.dump(report,report_file,indent=4,ensure_ascii=False)
