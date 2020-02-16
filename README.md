# keledge_pdf
可知PDF下载解密合并脚本，下载电子工业出版社 悦读平台PDF的弯道超车方法 =，=

# 免责声明

**请自觉遵守法律法规，本脚本仅供学习参考，所有下载的PDF请在24小时内删除，请勿传播，一切法律责任由用户自己承担，与本人无关**

# APP端

## 时间记录

### 2020年2月16日 10:30

可知 安卓平台 2.2.6 版本 依然可以成功解密

## 参考资料

- [下载电子工业出版社开放出来的电子书](https://github.com/hanxi/blog/issues/44)
- [电子工业出版社“悦读”PDF下载](https://github.com/shylocks/51zhy_pdf)  

## 可知/悦读

**可知官网**：[http://keledge.com](http://keledge.com)  

**悦读官网**：[http://yd.51zhy.cn](http://yd.51zhy.cn)  

之前审查元素的时候发现**悦读**官方给的手机客户端下载链接指向的是**可知** ，然后就这样 **可知** 这个平台被我们注意到了，经过几次加密方式的变更，判断出**悦读**和**可知**应该是同一批程序员小哥维护的 =，= 本文就是利用这个思路 用曾经网上公开的解密 悦读的方法后 再来解密 可知。

## 准备工作

- 可知 安卓APP 2.2.6 版本   [蓝奏云](https://www.lanzous.com/i9e7jxc)   [华为应用市场](https://appstore.huawei.com/app/C100372899)
- 一个顺手的抓包工具   

**关于APP** 2.2.6这个版本是加密方式变更之前的版本，所以加密方式还很古老，可以轻松解密，升级最新的2.8.8版本后就会像在电脑端操作一样，需要浏览器debug去找RSA的私钥，虽然这样操作也可以，但是操作门槛要高上许多。

**关于抓包** 国光一直用Burpsuite来抓包，有些朋友推荐的Fiddler也是可以的，甚至安卓平台上的HttpCanary是可以抓包的

## 抓包的坑

这里我提一下几个关键点，

1. Burpsuite的证书得手动改为 `crt`后缀 手机才可以顺利安装
2. 电脑和手机可以IP互通 即可抓包 无需安卓模拟器 只要手机代理地址 手工填写BP的IP即可

## 解密复现

### 准备抓包

APP上找到想要阅读的书籍，到这个界面，然后开启抓包后，点击 **在线试读**  这里会有一个关键的认证包

![](imgs/15818189145984.jpg) 

### 认证分析

关键的认证包如下：

![](imgs/15818191372934.jpg) 

下面贴上关键的明文数据包情况

**请求包**

```
POST /aqr/authorize HTTP/1.1
Accept-Language: zh-CN,zh;q=0.8
User-Agent: Mozilla/5.0 (Linux; U; Android 10; zh-cn; Redmi K20 Build/QKQ1.190825.002) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 1130
Host: api.keledge.com
Connection: close
Accept-Encoding: gzip, deflate

AuthorzieParameters=%7B%22ContentExternalId%22%3A%22P00003-01-45957-Pdf%22%2C%22Device%22%3A%7B%22DeviceKey%22%3A%22xeWAeZ%7D%3A%3F%5Cu003dy_c%28B0%22%2C
```

**返回包**

```json
HTTP/1.1 200 OK
Server: nginx
Date: Sun, 16 Feb 2020 02:10:53 GMT
Content-Type: application/json; charset=utf-8
Connection: close
Vary: Accept-Encoding
Cache-Control: private
X-AspNetMvc-Version: 5.2
X-AspNet-Version: 4.0.30319
Access-Control-Allow-Origin: *
Access-Control-Allow-Headers: *
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Content-Length: 356780

{
  "Success": true,
  "Code": 200,
  "Description": "成功",
  "Data": {
    "Key": "QMXErurDVc9FUeIDSaSsf/RqTg3qZScwYiMX7GZ6INs=",
    "Url": "http://",
    "FileId": 562299107666825218,
    "IsOnline": true,
    "FileFormat": ".pdf",
    "AuthorizeStrategy": {
      "UsageType": 1,
      "AllowReadPercentage": 1.0,
      "RealityReadPercentage": 0.10,
      "RequiredValidateTime": "2020-03-16 10:10:53"
    },
   ...
   ...
}
```

### 找到DeviceKey

上面请求包中包含了DeviceKey，具体如下：

```
DeviceKey%22%3A%22xeWAeZ%7D%3A%3F%5Cu003dy_c%28B0%22%2C
```

这看上去可能会比较奇怪，这里我们先对其进行URL解码，得到如下内容：

```json
DeviceKey":"xeWAeZ}:?\u003dy_c(B0",
```

拿到DeviceKey的值为：`xeWAeZ}:?\u003dy_c(B0`  看上去还是很奇怪，这里并不是16位，那么这个`\u003d`肯定被编码了，JS里面`alert('\u003d')`解码看看：

![](imgs/15818195705736.jpg)  

发现这是一个等于号，所以最终的DeviceKey如下：

```json
DeviceKey":"xeWAeZ}:?=y_c(B0",
```

### 解密书籍的Key

返回包里面可以看到每个书籍对应的Key值：

```json
"Key": "QMXErurDVc9FUeIDSaSsf/RqTg3qZScwYiMX7GZ6INs="
```

使用`DeviceKey`来解密这个`Key`试试看

#### 在线解密

[AES在线加密解密](https://oktools.net/aes)

![](https://image.3001.net/images/20200216/15818198937406.jpg)  

拿到解密后的秘钥为：

```
$@6^O8bbWD^VcSJz
```

#### 其他解密思路

Linux 或者 macOS终端下运行，该命令核心是借助openssl解密，Windows虽然原生没有openssl 但是也是可以自己折腾一下的：

```bash
echo 'QMXErurDVc9FUeIDSaSsf/RqTg3qZScwYiMX7GZ6INs=' | openssl enc -d -aes-128-ecb -a -K 78655741655a7d3a3f3d795f63284230
```

> 78655741655a7d3a3f3d795f63284230 这个是DeviceKey先ascii然后再hex编码后的值

输出结果：

```
$@6^O8bbWD^VcSJz
```

### 解密单页

返回包的这个字段里面放着 每页PDF对应的地址

```json
"SplitFileUrls": [
        "https://ptpress.keledge.com:50002/transfer/dcd/net/content/stream?q=Yjqzhk4LiuBpUhVJNwdWtgjGBNHymFKm80RenEPO8N%2bo17FQgBBANunYozQFDZUAP8if%2fwnoxvLGQ3zSzC4%2f6wAnsDs%2bwHnGDsezbdSLDro%3d&BridgePlatformName=aqrcloud_web&fn=E4NUiNc0a7ojQA6gdxCKTg==",
        "https://ptpress.keledge.com:50002/transfer/dcd/net/content/stream?q=Yjqzhk4LiuBpUhVJNwdWtgjGBNHymFKm80RenEPO8N%2bo17FQgBBANunYozQFDZUAPQA%2fHI9%2bk6RjUHXlP2ue3AAnsDs%2bwHnGDsezbdSLDro%3d&BridgePlatformName=aqrcloud_web&fn=SSMLUKmbQ0zn41dYgOIpkQ==",
  ...
  ...
]
```

这里直接下载一个到本地，手动重命名为`encode.pdf`

先把上面拿到的aes秘钥给ascii编码再hex编码一下：

```
$@6^O8bbWD^VcSJz
```

编码后为：

```
2440365e4f38626257445e5663534a7a
```

Python简单实现ascii再hex编码的Demo为：

```python
hex_ascii_key = ''
for i in '$@6^O8bbWD^VcSJz':
    hex_ascii_key += f'{ord(i):x}'
print(hex_ascii_key)
```

命令行下依然使用openssl来解密pdf:

```
➜ openssl enc -d -aes-128-ecb -K 2440365e4f38626257445e5663534a7a -in encode.pdf -out decode.pdf
```

将`encode.pdf`解密后导出为`decode.pdf`  如果没有报错的话 说明解密就成功了

![](imgs/15818207376284.jpg) 

解密成功，开始尝试批量解密

## 脚本解密

实际上脚本基本上不用怎么改，国光我依然用的是之前写的脚本，实际上和之前的代码基本上一样，只是这里发现不需要headers头也可以访问请求下载PDF了，所以就顺便删了相关代码，代码更简便一些了。

参考项目里面的 [keledge_android.py](keledge_android.py)

## PDF/EPUB

这里说解密过程中的几个关键点：

1. APP在线阅读默认是阅读epub格式的，点击右下角的小箭头 可以手动选择在线阅读pdf
2. epub的返回包比较神奇，有的可以看到**完整的**epub下载地址 没错是完整的
3. epub加密比较特殊，首先binwalk分析发现是zip头 解压后 发现图片没有加密 所以只解密xhtml或者html格式的文档就可以了 然后解密完重新打包成epub格式即可

## 总结

本文抓包部分上手难度比较高，折腾需谨慎。

国光建议书籍的话 还是找自己需要的书籍比较合适，书再多 看不完 也没有什么用 对吧

另外 可知 悦读的程序员小哥辛苦了 这几天肯定又通宵加班了 (心疼3秒钟)

# PC端

## 时间记录

### 2020年2月10日 15.30

浏览器前端已经获取不到RSA的私钥了 =，=  看来是凉透了

### 2020年2月10日 07:26

可知平台暂时关闭开放阅读了 书籍全部采用部分试读（和悦读的操作一样） =，= 只能采用APP端阅读

大家可以关注一下这位大佬的项目 已经开始适配可知平台了 

https://github.com/shylocks/51zhy_pdf 

本项目 应该咸鱼了 我的任务完成了 =，= 

## 手工复现

可知官网 : https://www.keledge.com

这个平台书籍很全 包含了电子工业出版社、化学工业出版社、人民邮电出版社、社会科学文献出版社的一些书籍，其中书籍一般是以PDF或者EPUB格式公开给读者阅读了，PDF本身是加密的，浏览器JS解密后供读者来阅读。

### 原理

PDF 分页使用AES来加密的，解密需要AES的KEY值，这个KEY加密后的值 经过抓包分析也可以得到，解密这个KEY的话 需要RSA来解密，RSA的公私钥浏览器均可以看到。所以 整个解密流程如下：

1. 获取RSA的公私钥
2. 找到PDF加密后的KEY值
3. 解密KEY值
4. 然后AES来解密PDF

### 1. 获取公私钥

「审查元素」-「Application」-「Cookies」-「https://www.keledge.com」-「rsaKeys」

![](imgs/158123899365.png)  

获取的的rsaKeys的值如下：

```bash
%7B%22privateKey%22%3A%22-----BEGIN%20RSA%20PRIVATE%20KEY-----%5Cr%5CnMIIEogIBAAKCAQEAgjhYN8nU9A9IgA6zwggq6wG3tISazCcZ2uicV20wu2jlZw%2BG%5Cr%5Cnj3y7Y7Bx3E62fCHy5wdC9h1qOdRmtvu8adZZ3dYWuJBYldIPs39OByrhI3sRGfkv%5Cr%5CnoCs785Db8wJlrwlgbi5OiEfjy6OuK9B6DFUhYSCmqHbXefK4xcAA5QM74K4c3%2Bez%5Cr%5CnqZv6%2BRXuGImGSQtCcgnXXnn%2BHHviiiWPeEzX0ilwN8xbUEKhZrvKUcosFiZ5ddO%2F%5Cr%5Cn7X7QOuaReX0oBxvEfyjaPG5UFze6gW3bDMiIYQWoWQX0jbpMBDq0jnzaBe6dg9la%5Cr%5CnMgGcINn6PC8jqowRSHGWfhChEfJIB%2FAEgYxuGwIBAwKCAQBW0DrP2%2BNNX4WqtHfW%5Cr%5CnsBycq8%2FNrbyIGhE8mxLk83XSRe5EtQRfqHztIEvoNHmoFqHvWiykE5wmjZnPUn2b%5Cr%5Cn5DvpOWR7CuW5NrUiVN6vcets%2FLYRUMpqx31NCz1MrEPKBkBJdDRa2pfdF8lyivwI%5Cr%5CnOMDraxnFpI%2BmodCD1VXuAifrHbzeXATGfGac%2BUKwJrjMYr5yJTM5yEyFrT6E2FAt%5Cr%5CnDXIa8C9X4w9fhP6fRsQ0m4HImKVUG60SVf%2BdBgE1k2pIXhVWx2UybSUAsKstosNf%5Cr%5CneJKXJ2pNOcYS0og0im3ulRmEQWtIlPJT%2BPMAVclJ3%2BckILsRqRhM5w6qFWxSQVfw%5Cr%5Cnk4KbAoGBAP6sWfkqvFB2v%2F2%2BrLZ2BWafVUHcY7g%2FyUOCcbbYJy1FUVxn8G0AzXpm%5Cr%5CndFytCPSqCuxdBzN2PNJ%2FfIEZdiQ57vndH%2FEZKYHxyESKwHE7LGKpFmDtzTfZmfC4%5Cr%5CnHtgBqide8tqSYOvMTEYDikmrPlfp5lozmsP8RINQu%2BObfaKBd15XAoGBAILmA7NV%5Cr%5CnJRCW4AxRorqgcb4nfMiradMULsFAb2BckX9kb8zMB1dALakRXUdV1%2FS%2FNpUaowjb%5Cr%5CnwP5P4Q6PqeRgn6qf3dFXoRqkZnUyOUTCZ0nVNCf3YhOX5I79TDem8wxgmaIEmQLn%5Cr%5Cnv%2BmczwKiIPEKdJ56WS4OcYfCFkHxEF4XN8vdAoGBAKnIO%2Ftx0uBPKqkpyHmkA5m%2F%5Cr%5CnjivoQnrVMNesS886xMjY4OhFSvNV3lGZouhzW03GsfLor3ekKIxU%2FatmTsLRSfvo%5Cr%5Cnv%2FYQxlahMC2x1aDSHZcbZECeiM%2FmZqB6vzqrxsTp9zxhlfKIMtlXsYZyKY%2FxRDwi%5Cr%5CnZy1S2FeLJ%2B0SU8GrpOmPAoGAV0QCd44YtbnqsuEXJxWhKW%2Bohceb4g10gNWflZML%5Cr%5CnqkL1MzKvj4AecLY%2BL46P%2BH95uLxssJKAqYqWCbUb7ZW%2FxxU%2Bi4%2FAvG2Zo3bQ2IGa%5Cr%5CnMTjNb%2FpBYmVDCf4yz8SiCEBmbAMQrJp%2F8RM0rGwV9gb4aabmHrRLr9a5gUtgProl%5Cr%5CnMpMCgYEAwvZwwpe2A0YwC9mzpRKs8io3tt%2BZzEdeKJiZwh%2Btme2BWAvMMpFbXbUc%5Cr%5Cnz9tZHEFp5HVHLcQZ13QrbFR6dWsd38W0VEBs%2FVds3LNTORIB54sJowncPDSO3jhk%5Cr%5CnGAAoLX0of5awRL8zj4eibt%2FVN3M%2F5%2F%2FXou5ffLKUQCsinigEO38%3D%5Cr%5Cn-----END%20RSA%20PRIVATE%20KEY-----%5Cr%5Cn%22%2C%22publicKey%22%3A%22-----BEGIN%20PUBLIC%20KEY-----%5Cr%5CnMIIBIDANBgkqhkiG9w0BAQEFAAOCAQ0AMIIBCAKCAQEAgjhYN8nU9A9IgA6zwggq%5Cr%5Cn6wG3tISazCcZ2uicV20wu2jlZw%2BGj3y7Y7Bx3E62fCHy5wdC9h1qOdRmtvu8adZZ%5Cr%5Cn3dYWuJBYldIPs39OByrhI3sRGfkvoCs785Db8wJlrwlgbi5OiEfjy6OuK9B6DFUh%5Cr%5CnYSCmqHbXefK4xcAA5QM74K4c3%2BezqZv6%2BRXuGImGSQtCcgnXXnn%2BHHviiiWPeEzX%5Cr%5Cn0ilwN8xbUEKhZrvKUcosFiZ5ddO%2F7X7QOuaReX0oBxvEfyjaPG5UFze6gW3bDMiI%5Cr%5CnYQWoWQX0jbpMBDq0jnzaBe6dg9laMgGcINn6PC8jqowRSHGWfhChEfJIB%2FAEgYxu%5Cr%5CnGwIBAw%3D%3D%5Cr%5Cn-----END%20PUBLIC%20KEY-----%5Cr%5Cn%22%7D
```

经过 URL解码后如下：

```
{"privateKey":"-----BEGIN RSA PRIVATE KEY-----\r\nMIIEogIBAAKCAQEAgjhYN8nU9A9IgA6zwggq6wG3tISazCcZ2uicV20wu2jlZw+G\r\nj3y7Y7Bx3E62fCHy5wdC9h1qOdRmtvu8adZZ3dYWuJBYldIPs39OByrhI3sRGfkv\r\noCs785Db8wJlrwlgbi5OiEfjy6OuK9B6DFUhYSCmqHbXefK4xcAA5QM74K4c3+ez\r\nqZv6+RXuGImGSQtCcgnXXnn+HHviiiWPeEzX0ilwN8xbUEKhZrvKUcosFiZ5ddO/\r\n7X7QOuaReX0oBxvEfyjaPG5UFze6gW3bDMiIYQWoWQX0jbpMBDq0jnzaBe6dg9la\r\nMgGcINn6PC8jqowRSHGWfhChEfJIB/AEgYxuGwIBAwKCAQBW0DrP2+NNX4WqtHfW\r\nsBycq8/NrbyIGhE8mxLk83XSRe5EtQRfqHztIEvoNHmoFqHvWiykE5wmjZnPUn2b\r\n5DvpOWR7CuW5NrUiVN6vcets/LYRUMpqx31NCz1MrEPKBkBJdDRa2pfdF8lyivwI\r\nOMDraxnFpI+modCD1VXuAifrHbzeXATGfGac+UKwJrjMYr5yJTM5yEyFrT6E2FAt\r\nDXIa8C9X4w9fhP6fRsQ0m4HImKVUG60SVf+dBgE1k2pIXhVWx2UybSUAsKstosNf\r\neJKXJ2pNOcYS0og0im3ulRmEQWtIlPJT+PMAVclJ3+ckILsRqRhM5w6qFWxSQVfw\r\nk4KbAoGBAP6sWfkqvFB2v/2+rLZ2BWafVUHcY7g/yUOCcbbYJy1FUVxn8G0AzXpm\r\ndFytCPSqCuxdBzN2PNJ/fIEZdiQ57vndH/EZKYHxyESKwHE7LGKpFmDtzTfZmfC4\r\nHtgBqide8tqSYOvMTEYDikmrPlfp5lozmsP8RINQu+ObfaKBd15XAoGBAILmA7NV\r\nJRCW4AxRorqgcb4nfMiradMULsFAb2BckX9kb8zMB1dALakRXUdV1/S/NpUaowjb\r\nwP5P4Q6PqeRgn6qf3dFXoRqkZnUyOUTCZ0nVNCf3YhOX5I79TDem8wxgmaIEmQLn\r\nv+mczwKiIPEKdJ56WS4OcYfCFkHxEF4XN8vdAoGBAKnIO/tx0uBPKqkpyHmkA5m/\r\njivoQnrVMNesS886xMjY4OhFSvNV3lGZouhzW03GsfLor3ekKIxU/atmTsLRSfvo\r\nv/YQxlahMC2x1aDSHZcbZECeiM/mZqB6vzqrxsTp9zxhlfKIMtlXsYZyKY/xRDwi\r\nZy1S2FeLJ+0SU8GrpOmPAoGAV0QCd44YtbnqsuEXJxWhKW+ohceb4g10gNWflZML\r\nqkL1MzKvj4AecLY+L46P+H95uLxssJKAqYqWCbUb7ZW/xxU+i4/AvG2Zo3bQ2IGa\r\nMTjNb/pBYmVDCf4yz8SiCEBmbAMQrJp/8RM0rGwV9gb4aabmHrRLr9a5gUtgProl\r\nMpMCgYEAwvZwwpe2A0YwC9mzpRKs8io3tt+ZzEdeKJiZwh+tme2BWAvMMpFbXbUc\r\nz9tZHEFp5HVHLcQZ13QrbFR6dWsd38W0VEBs/Vds3LNTORIB54sJowncPDSO3jhk\r\nGAAoLX0of5awRL8zj4eibt/VN3M/5//Xou5ffLKUQCsinigEO38=\r\n-----END RSA PRIVATE KEY-----\r\n","publicKey":"-----BEGIN PUBLIC KEY-----\r\nMIIBIDANBgkqhkiG9w0BAQEFAAOCAQ0AMIIBCAKCAQEAgjhYN8nU9A9IgA6zwggq\r\n6wG3tISazCcZ2uicV20wu2jlZw+Gj3y7Y7Bx3E62fCHy5wdC9h1qOdRmtvu8adZZ\r\n3dYWuJBYldIPs39OByrhI3sRGfkvoCs785Db8wJlrwlgbi5OiEfjy6OuK9B6DFUh\r\nYSCmqHbXefK4xcAA5QM74K4c3+ezqZv6+RXuGImGSQtCcgnXXnn+HHviiiWPeEzX\r\n0ilwN8xbUEKhZrvKUcosFiZ5ddO/7X7QOuaReX0oBxvEfyjaPG5UFze6gW3bDMiI\r\nYQWoWQX0jbpMBDq0jnzaBe6dg9laMgGcINn6PC8jqowRSHGWfhChEfJIB/AEgYxu\r\nGwIBAw==\r\n-----END PUBLIC KEY-----\r\n"}
```

编辑器批量将`\r\n`替换为空最后如下：

#### privateKey

```
-----BEGIN RSA PRIVATE KEY-----MIIEogIBAAKCAQEAgjhYN8nU9A9IgA6zwggq6wG3tISazCcZ2uicV20wu2jlZw+Gj3y7Y7Bx3E62fCHy5wdC9h1qOdRmtvu8adZZ3dYWuJBYldIPs39OByrhI3sRGfkvoCs785Db8wJlrwlgbi5OiEfjy6OuK9B6DFUhYSCmqHbXefK4xcAA5QM74K4c3+ezqZv6+RXuGImGSQtCcgnXXnn+HHviiiWPeEzX0ilwN8xbUEKhZrvKUcosFiZ5ddO/7X7QOuaReX0oBxvEfyjaPG5UFze6gW3bDMiIYQWoWQX0jbpMBDq0jnzaBe6dg9laMgGcINn6PC8jqowRSHGWfhChEfJIB/AEgYxuGwIBAwKCAQBW0DrP2+NNX4WqtHfWsBycq8/NrbyIGhE8mxLk83XSRe5EtQRfqHztIEvoNHmoFqHvWiykE5wmjZnPUn2b5DvpOWR7CuW5NrUiVN6vcets/LYRUMpqx31NCz1MrEPKBkBJdDRa2pfdF8lyivwIOMDraxnFpI+modCD1VXuAifrHbzeXATGfGac+UKwJrjMYr5yJTM5yEyFrT6E2FAtDXIa8C9X4w9fhP6fRsQ0m4HImKVUG60SVf+dBgE1k2pIXhVWx2UybSUAsKstosNfeJKXJ2pNOcYS0og0im3ulRmEQWtIlPJT+PMAVclJ3+ckILsRqRhM5w6qFWxSQVfwk4KbAoGBAP6sWfkqvFB2v/2+rLZ2BWafVUHcY7g/yUOCcbbYJy1FUVxn8G0AzXpmdFytCPSqCuxdBzN2PNJ/fIEZdiQ57vndH/EZKYHxyESKwHE7LGKpFmDtzTfZmfC4HtgBqide8tqSYOvMTEYDikmrPlfp5lozmsP8RINQu+ObfaKBd15XAoGBAILmA7NVJRCW4AxRorqgcb4nfMiradMULsFAb2BckX9kb8zMB1dALakRXUdV1/S/NpUaowjbwP5P4Q6PqeRgn6qf3dFXoRqkZnUyOUTCZ0nVNCf3YhOX5I79TDem8wxgmaIEmQLnv+mczwKiIPEKdJ56WS4OcYfCFkHxEF4XN8vdAoGBAKnIO/tx0uBPKqkpyHmkA5m/jivoQnrVMNesS886xMjY4OhFSvNV3lGZouhzW03GsfLor3ekKIxU/atmTsLRSfvov/YQxlahMC2x1aDSHZcbZECeiM/mZqB6vzqrxsTp9zxhlfKIMtlXsYZyKY/xRDwiZy1S2FeLJ+0SU8GrpOmPAoGAV0QCd44YtbnqsuEXJxWhKW+ohceb4g10gNWflZMLqkL1MzKvj4AecLY+L46P+H95uLxssJKAqYqWCbUb7ZW/xxU+i4/AvG2Zo3bQ2IGaMTjNb/pBYmVDCf4yz8SiCEBmbAMQrJp/8RM0rGwV9gb4aabmHrRLr9a5gUtgProlMpMCgYEAwvZwwpe2A0YwC9mzpRKs8io3tt+ZzEdeKJiZwh+tme2BWAvMMpFbXbUcz9tZHEFp5HVHLcQZ13QrbFR6dWsd38W0VEBs/Vds3LNTORIB54sJowncPDSO3jhkGAAoLX0of5awRL8zj4eibt/VN3M/5//Xou5ffLKUQCsinigEO38=-----END RSA PRIVATE KEY-----
```

#### publicKey

```
-----BEGIN PUBLIC KEY-----MIIBIDANBgkqhkiG9w0BAQEFAAOCAQ0AMIIBCAKCAQEAgjhYN8nU9A9IgA6zwggq6wG3tISazCcZ2uicV20wu2jlZw+Gj3y7Y7Bx3E62fCHy5wdC9h1qOdRmtvu8adZZ3dYWuJBYldIPs39OByrhI3sRGfkvoCs785Db8wJlrwlgbi5OiEfjy6OuK9B6DFUhYSCmqHbXefK4xcAA5QM74K4c3+ezqZv6+RXuGImGSQtCcgnXXnn+HHviiiWPeEzX0ilwN8xbUEKhZrvKUcosFiZ5ddO/7X7QOuaReX0oBxvEfyjaPG5UFze6gW3bDMiIYQWoWQX0jbpMBDq0jnzaBe6dg9laMgGcINn6PC8jqowRSHGWfhChEfJIB/AEgYxuGwIBAw==-----END PUBLIC KEY-----
```

### 2. 获取PDF的加密KEY值

这里我们用电子工业出版社的这本书来举例子：[中国互联网发展报告2019](https://www.keledge.com/wrap/details/book?id=656844567328329728)  

点击在线阅读后 按照如下图所示来 审查元素：

![](imgs/15812395549752.jpg)  

这个Response的内容很重要，里面不仅记录了每个PDF对应的KEY值，还对应着PDF每页的下载地址，下面只展示部分：

```json
{
  "Success": true,
  "Code": 200,
  "Description": "成功",
  "Data": {
    "Key": "Ntp0a6YsGzw5OlyGdoV/Oi3i/gmDQjfJfDpfakxpk0NqvWQHvwMdheijy5lqskIx2NTuYcalitKSBKSICbNZtaGwAEvXuR4OPpiXxJHhXa2MQmYjUIL4Yc/anYlGNWk3x/40HTfV2tMcz9oOI/6jKDmw1Ld8H3eP79dxxDyqkrxLGJbgjoxG3pHEY4YiBrlM5mqNm82xac6KE0kOZ8kScTu8dIDX/M2ae+AE7Y2M+tTTfvRXleCIm3sDQ/xLP7TNX/rdtVQE+lKzoEmvwUzmCCkqnmuEIFtHYJiESLmuNiJNDk+HBt06xIneAgO1/J6ye2HYiyDWlYbaz91wk3pemQ==",
    "Url": "http://",  // 实际上这里很可能是完整的PDF地址 但是被机智的程序员小哥删掉了
    "FileId": 656832800904712192,
    "IsOnline": true,
    "FileFormat": ".pdf",
    "AuthorizeStrategy": {
      "UsageType": 1,
      "AllowReadPercentage": 1.0,
      "RealityReadPercentage": 0.20,
      "RequiredValidateTime": "2020-03-09 17:11:24"
    },
    "NumberOfPages": 492,
    "SplitFiles": [
      {
    			...
      {
      ,
    "SplitFileUrls": [
					...
			]
			}
}
```

#### Key

提取出KEY值如下：

```
Ntp0a6YsGzw5OlyGdoV/Oi3i/gmDQjfJfDpfakxpk0NqvWQHvwMdheijy5lqskIx2NTuYcalitKSBKSICbNZtaGwAEvXuR4OPpiXxJHhXa2MQmYjUIL4Yc/anYlGNWk3x/40HTfV2tMcz9oOI/6jKDmw1Ld8H3eP79dxxDyqkrxLGJbgjoxG3pHEY4YiBrlM5mqNm82xac6KE0kOZ8kScTu8dIDX/M2ae+AE7Y2M+tTTfvRXleCIm3sDQ/xLP7TNX/rdtVQE+lKzoEmvwUzmCCkqnmuEIFtHYJiESLmuNiJNDk+HBt06xIneAgO1/J6ye2HYiyDWlYbaz91wk3pemQ==
```

### 3. 解密KEY值

这里使用在线工具来进行RSA解密KEY值：https://oktools.net/rsa  

![](imgs/15812401279480.jpg)  

拿到key的明文为：

```
lHVrM9iO9Y9_#MOl
```

### 4. 解密PDF

首先先下载一页PDF，PDF的每页信息就在之前的Response的信息里面：

```json
"SplitFileUrls": [
      "https://phei.keledge.com:50002/transfer/dcd/net/content/stream?q=Yjqzhk4LiuBpUhVJNwdWtm%2fJLn8sTFIekEjbID01RfZvVs%2fuTgVg30fHFL60N6c8LPMfyoiIILhkpCB3%2fCL%2bmK1R9Up1uvOJ6zfgmwfRGVr1tgIvWqUNT2KmAe%2bNF6kU&BridgePlatformName=aqrcloud_web&fn=E4NUiNc0a7ojQA6gdxCKTg==",
      "https://phei.keledge.com:50002/transfer/dcd/net/content/stream?q=Yjqzhk4LiuBpUhVJNwdWtm%2fJLn8sTFIekEjbID01RfZvVs%2fuTgVg30fHFL60N6c8LPMfyoiIILhkpCB3%2fCL%2bmLHwdoCFWtjmghlQXyxcI6j1tgIvWqUNT2KmAe%2bNF6kU&BridgePlatformName=aqrcloud_web&fn=SSMLUKmbQ0zn41dYgOIpkQ==",
      "https://phei.keledge.com:50002/transfer/dcd/net/content/stream?q=Yjqzhk4LiuBpUhVJNwdWtm%2fJLn8sTFIekEjbID01RfZvVs%2fuTgVg30fHFL60N6c8LPMfyoiIILhkpCB3%2fCL%2bmHv9C20Q34lGZwBnIaa%2bQCT1tgIvWqUNT2KmAe%2bNF6kU&BridgePlatformName=aqrcloud_web&fn=UaErHZOI2duPfr8G6oC3rQ==",
]
```

浏览器访问1页下载下来，国光这里使用的是openssl来进行aes解密的：

```
➜ openssl enc -d -aes-128-ecb -K 6c4856724d39694f3959395f234d4f6c -in 下载的PDF文件.pdf -out out.pdf
```

> -K 6c4856724d39694f3959395f234d4f6c 这里的K值就是 我们之前的 `lHVrM9iO9Y9_#MOl` ascii后再hex编码的值

来康康 out.pdf  成功！ 下面尝试来脚本自动化吧：

![](imgs/15812406177996.jpg)    



## 简化脚本

本脚本为Python3脚本，

### 依赖安装

```bash
requests==2.22.0
progressbar33==2.4
PyPDF2==1.26.0
```

保存为`requirements.txt`文件，然后安装相关的依赖模块：

```bash
pip install -r requirements.txt
```

### openssl

因为代码里面使用了openssl来解密，所以需要系统环境有openssl，在Linux或者macOS上都可以很轻易使用，Windows平台也有openssl 这里需要大家自行去折腾一下，然后更改对应的代码：

```python
os.system(f'mkdir {tmp_dir}')

os.system(f'openssl enc -d -aes-128-ecb -K {hex_ascii_key } -in {tmp_dir}/{filename}.aes -out {tmp_dir}/{filename}.pdf')

os.system(f'rm {tmp_dir}/*.aes')

os.system(f'rm -rf {tmp_dir}')
```

这些命令都需要自行更换为Windows下可以执行的命令

### Too many open files 异常

在执行多线程合并PDF的时候可能出现如下问题：

```
正在合成PDF文件.........
Traceback (most recent call last):
  File "keledge.py", line 94, in <module>
  File "keledge.py", line 75, in main
  File "/Users/sqlsec/.pyenv/versions/3.6.6/lib/python3.6/site-packages/PyPDF2/merger.py", line 203, in append
  File "/Users/sqlsec/.pyenv/versions/3.6.6/lib/python3.6/site-packages/PyPDF2/merger.py", line 114, in merge
OSError: [Errno 24] Too many open files: 'download_3c35af8c-85bc-4713-a91b-32df2f0a150a/x-253.pdf'
```

这是因为达到系统文件的占用上线了，这里我们可以手动修改大一点的值：

```bash
ulimit -n 3000
```

然后就可以正常合并PDF了

### 源码

```python
import os
import json
import uuid
import argparse
import requests
import progressbar
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter

def main():
    # 命令行说明
    parser= argparse.ArgumentParser()
    parser.add_argument('-k','--key',dest='key',help="input the key")
    parser.add_argument('-n','--name',dest='name',help="input books's name")
    parser.add_argument('-s','--source',dest='source')
    args = parser.parse_args()

    if args.key == None or args.name == None:
        parser.print_help()
        os._exit(0)

    if args.source == None:
        args.source = "phei"

    else:
        args.source = "ptpress"

    # key先ascii然后再hex
    hex_ascii_key = ''
    for i in args.key:
        hex_ascii_key += f'{ord(i):x}'
    
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
        'Connection': 'keep-alive',
        'Cookie': '!!!!****这里填入你们自己的Cookie****!!!',
        'Host': '{source}.keledge.com:50002'.format(source=args.source),
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
    }

    # 加载json请求
    try:
        with open('res.json', 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(e)

    bookurls = data['Data']['SplitFileUrls']
    uuid_str = uuid.uuid4()
    tmp_dir = 'download_%s' % uuid_str
    os.system(f'mkdir {tmp_dir}')

    p = progressbar.ProgressBar()
    for url in p(bookurls):
        page = bookurls.index(url)+1
        filename = f"x-{page}"
        r = requests.get(url = url,headers=headers,stream=True)
        with open(tmp_dir + '/' + filename+'.aes','wb') as f:
            f.write(r.content)
        os.system(f'openssl enc -d -aes-128-ecb -K {hex_ascii_key } -in {tmp_dir}/{filename}.aes -out {tmp_dir}/{filename}.pdf')
        os.system(f'rm {tmp_dir}/*.aes')
    
    print("正在合成PDF文件.........")
    for root, dirs, files in os.walk(tmp_dir):
        if '.DS_Store' in files:
            files.remove('.DS_Store')
        files.sort(key=lambda x: int(x[x.rfind('-') + 1:][:-4]))
        file_list = [tmp_dir + '/' + file for file in files]
        merger = PdfFileMerger(strict=False)
        for pdf in file_list:
            merger.append(pdf)
        path = args.name + '.pdf'
        merger.write(path)
    print("Success !!!!")
    os.system(f'rm -rf {tmp_dir}')

if __name__ == "__main__":
    logo = '''\033[0;32m
 __  ___  _______  __       _______  _______   _______  _______ 
|  |/  / |   ____||  |     |   ____||       \ /  _____||   ____|
|  '  /  |  |__   |  |     |  |__   |  .--.  |  |  __  |  |__   
|    <   |   __|  |  |     |   __|  |  |  |  |  | |_ | |   __|  
|  .  \  |  |____ |  `----.|  |____ |  '--'  |  |__| | |  |____ 
|__|\__\ |_______||_______||_______||_______/ \______| |_______|  

        https://www.sqlsec.com/2020/02/keledge.html
                                     
    \033[0m'''
    print(logo)
    main()
```

### 使用说明

#### 填入自己的Cookie

```python
 headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
        'Connection': 'keep-alive',
        'Cookie': '!!!!****这里填入你们自己的Cookie****!!!',
        'Host': '{source}.keledge.com:50002'.format(source=args.source),
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
    }
```

下载PDF的请求头 写入自己的Cookie

#### 手动保存res.json

[获取PDF的加密KEY值](https://www.sqlsec.com/2020/02/keledge.html#toc-heading-7)  

前面提到了这个返回头很重要，我们手动保存到当前脚本的同级目录下为`res.json`，因为这里代码写死了 

=，= ：

```python
    # 加载json请求
    try:
        with open('res.json', 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(e)
```

#### 下载电子工业出版社

```bash
➜  1
➜  1 ls
keledge.py       requirements.txt res.json

# 电子工业出版社的PDF下载案例
➜  1 python keledge.py -k "lHVrM9iO9Y9_#MOl" -n "中国互联网发展报告2019"

➜  1 ls -l
total 656
-rw-r--r--@ 1 sqlsec  staff    3348  2  9 17:53 keledge.py
-rw-r--r--  1 sqlsec  staff      51  2  9 17:39 requirements.txt
-rw-r--r--@ 1 sqlsec  staff  307058  2  9 17:54 res.json
➜  1 python keledge.py -k "lHVrM9iO9Y9_#MOl" -n "中国互联网发展报告2019"

 __  ___  _______  __       _______  _______   _______  _______
|  |/  / |   ____||  |     |   ____||       \ /  _____||   ____|
|  '  /  |  |__   |  |     |  |__   |  .--.  |  |  __  |  |__
|    <   |   __|  |  |     |   __|  |  |  |  |  | |_ | |   __|
|  .  \  |  |____ |  `----.|  |____ |  '--'  |  |__| | |  |____
|__|\__\ |_______||_______||_______||_______/ \______| |_______|

        https://www.sqlsec.com/2020/02/keledge.html


  6% (31 of 492) |###                                                  | Elapsed Time: 0:00:12 ETA:   0:03:45
```

#### 下载人民邮电出版社

本脚本暂时只支持这两家出版社的书籍下载，原理实际上就是修改 请求头的`Host `值，这里脚本下载的话 手动添加`-s 2`参数就可以了，脚本默认是`-s 1`，

```bash
python keledge.py -k "KUt*YeeB6HOspx^B" -n "微信小程序开发实战" -s 2
```

![](imgs/15812428347743.jpg)  

## Flag 优化

实际上还可以添加目录的，但是可知普通的页码也被加密了，下面提供一下目录获取的接口地址。

### 可知

目录信息接口地址：

```
https://gateway.keledge.com/transfer/v1/api/tableofcontent/list
```

![](imgs/15812430927766.jpg)  

可以看到页码还是被单独加密了 =，=

### 悦读

目录信息接口地址：

```
https://bridge.51zhy.cn/transfer/tableofcontent/list
```

![](imgs/1581243230804.jpg)  

### 悦读脚本

```python
import fitz
import json

doc = fitz.open(r'book.pdf') 
toc = doc.getToC()

with open('bookmark.json', 'r') as f:
    data = json.load(f)

for i in data['Data']:
    level = i['ParentId']
    if level == 0:
        level = 1
    else:
        level = 2

    title = i['Title']
    page = i['Page']

    # 插入标题级别、标题、页数
    toc.append([level,title,page])

doc.setToC(toc)
doc.save(r'toc_book.pdf')
```

我发现这样可以设置目录级别：

```
for i in data['Data']:
    level = i['ParentId']
    if level == 0:
        level = 1
    else:
        level = 2
```

ParentId 为0的话 表明是1级目录，其他的都设置为2级，这样发现目录居然真的有效果：
但是只分了2级 2级和3级的区分就比较有难度了 可能我太菜了 没有发现明显的区分特征：

![](imgs/15812433556732.jpg)  

### 压缩

因为PDF是高清可以复制的版本，所以有很大的压缩空间，下面是国光的一个压缩测试：

![](imgs/15812434654672.jpg)  

😲 ！！！ 实际悦读效果还是不错的 在线压缩的网址是：

https://www.ilovepdf.com/zh-cn/compress_pdf  

## 总结

希望有大佬可以写出更自动化的脚本，比如添加目录 然后 压缩PDF 之类的，操作更简单一点，本文就当是抛砖引玉吧 溜了溜了 看书去了
