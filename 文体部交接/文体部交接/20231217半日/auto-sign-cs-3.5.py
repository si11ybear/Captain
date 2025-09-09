import re
import requests as rq
from pandas import DataFrame
from pandas import concat

def find_parameter(url,parameter):
    try:
        match = re.search(parameter + '=([0-9]+)', url)
    except:
        print('WRONG！请检查网址是否正确或联系开发人员雾路\n微信号：o8s16se34')
        input('按任意键结束')
        exit()
    return match.group(1)

def get_data(url):
    api='https://chexie.net/api/jiekouapi.php'
    bid=find_parameter(url,'bid')
    tid=find_parameter(url,'tid')
    data_info={
        'ask':'show',
        'ip':'0',
        'token':'0',
        'bid':bid,
        'tid':tid,
    }
    return rq.post(api,data=data_info).content.decode('utf-8')

def get_info(html_text):
    authors=re.findall('<author><!\[CDATA\[(.*?)\]\]></author>',html_text,flags=re.DOTALL)
    texts=re.findall('<text><!\[CDATA\[(.*?)\]\]></text>',html_text,flags=re.DOTALL)
    return authors,texts

def clean_text(text):
    clean_text=re.sub('<[/]?div.*?>','\n',text,flags=re.DOTALL)
    clean_text=re.sub('<br.*?>','\n',clean_text,flags=re.DOTALL)
    clean_text=re.sub('</p>','\n',clean_text,flags=re.DOTALL)
    clean_text=re.sub('&nbsp;',' ',clean_text,flags=re.DOTALL)
    clean_text=re.sub('<.*?>','',clean_text,flags=re.DOTALL)
    clean_text=re.sub('（可选.*）','',clean_text)
    return clean_text

def analyse_text(text):
    if_valid=len(re.findall('职务',text))>0
    if_quit=len(re.findall('<strike>',text))>0
    text=clean_text(text)
    match=re.findall('(.*)[:：](.*)',text)
    df=DataFrame(match)
    if if_valid:
        df.set_index(0,inplace=True)
        df=df.T
        df['是否已退出?(此处只记录楼层是否使用过删除线,具体内容还请到具体楼层确认!)']=if_quit
        df['分割线(右边的列是不正常格式的补充值,如果在左边的列中数据为NaN或空白,请在右边的列中查找相关数据)']='-----------'
    else:
        df=DataFrame([['NaN']],columns=[0])
    return df

def analyse_texts(authors,texts):
    df=DataFrame()
    for text in texts[1:]:
        df=concat([df,analyse_text(text)],ignore_index=True)
    df.index=authors[1:]
    return df

def divide_name_and_ID(text):
    match=re.match('(.*)[|｜∣丨ㅣ║│┃┊┋](.*)',text)
    name=re.sub('\s','',match.group(1))
    ID=re.sub('\s','',match.group(2))
    return name,ID

def split_nameID_column(df):
    df['姓名'],df['ID']=str(),str()
    for idx,nameID in enumerate(df['姓名|ID']):
        try:
            df.iloc[idx,-2],df.iloc[idx,-1]=divide_name_and_ID(nameID)
        except TypeError:
            pass
    df=df[['姓名','ID',*df.columns[1:-2]]]
    return df

print('''欢迎使用报名信息统计小助手!
        使用方法:
        1.根据提示输入相关网址
        2.根据提示输入相关参数
        3.等待程序运行完毕
        4.在程序所在文件夹中查看xls文件
        
        注意事项:
        1.请确保网址正确, 且网址中包含bid和tid参数
        2.获取xlsx文件后, 请使用Excel打开, 系统可能会出现文件格式相关提示, 忽视它, 继续打开文件
        3.如果出现乱码, 请使用Excel打开, 点击文件-另存为, 选择编码为UTF-8, 保存即可
        4.请注意xlsx文件中的第一列, 这是报名者在论坛上的ID, 如果此列ID与右方的ID不匹配, 请到具体楼层确认
        5.请注意xlsx文件中的分割线列, 如果左边的列中数据为NaN或空白, 请在右边的列中查找相关数据(这种情况一般是因为报名人员中的报名回复格式不规范)
        6.请注意xlsx文件中的'是否已退出?'列,
            如果为True, 说明该楼层已经使用过删除线, 可能是已经退出报名, 但也可能是楼主在报名回复中使用了删除线进行装饰, 具体情况请到具体楼层确认; 
            如果是False, 说明该楼层没有使用过删除线, 一般来说是没有退出报名的(不排除某些意外, 但概率极低)
        7.如果有任何问题, 请联系开发人员雾路, 微信号:o8s16se34
        
        现在, 请根据提示输入相关信息:
        ''')
url=input('1.请输入报名帖网址:')
raw_data=get_data(url)
activity_name=activity_name=re.findall('<title><!\[CDATA\[【(.*?)】',raw_data,flags=re.DOTALL)[0]
df=analyse_texts(*get_info(raw_data))
if_split=input('2.是否需要分离姓名和ID?(y/n)')
while True:
    if if_split=='y' or if_split=='Y' or if_split=='yes' or if_split=='Yes' or if_split=='YES':
        df=split_nameID_column(df)
        break
    elif if_split=='n' or if_split=='N' or if_split=='no' or if_split=='No' or if_split=='NO':
        break
    else:
        if_split=input('WRONG！请输入y或n')
    
df.to_excel(activity_name+'.xlsx')
print('已保存为\"'+activity_name+'.xlsx\"')
input('输入任意键退出。感谢你使用由<雾路|曹三省>制作的拉练报名信息统计工具。'
    '\n感谢参与测试人员：\n<余割|陈少春>\n<彤彤|侯依彤>\n<月霜|胡心月>\n<芊叶|王琴>\n如有疑问请联系微信c602\n微信号：o8s16se34')

    