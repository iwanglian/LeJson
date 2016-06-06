# LeJson
根据 `json` 文件,自动生成对应的数据模型,支持 `Objective-C` 和 `Java`.
配合 `mantle` 或 `gson` 等库使用,效果更佳.

## 最佳实践
### iOS
1. 在工程中创建 `Json` 目录, 存放所有的 `json`源文件, 不加入工程的target里.
2. 在工程中创建 `Model` 目录,存入所有自动生成的  `Model` 文件,加入工程target的compile source里.
3. 使用 `cocoapod` 导入 `MJExtension` 或 `YYModel`  `Mantle`
3. 在工程 `build phrase` 中新增一个 `run script`  ,放在 `complie source` 之前  
```bash
python <lejson.py_path> -d mj -o <model_path> <json_path>
```
4. 每次修改或新增 `json` 文件, 编译工程,就会自动生成相应的 `Model` 代码
5. 如果有新增的文件,手动加入到XCode工程中.

### Android
1. 在工程中创建 `Json` 目录, 存放所有的 `json`源文件,不加入编译 
2. 在工程中创建 `Model` 目录,存入所有自动生成的  `Model` 文件,加入到代码目录下.
3. 在`app`的 `build.gradle` 中引入 `gson` 或其它库 (`-d jo` 时不需要引入)
4. 在主工程的  `build.gradle` 加入 task:
```groovy
task lejsonJO(type: Exec) {
    commandLine 'python','<lejson.py_path>' ,'-d', 'jo', '-o', '<model_path>','<json_path>'
}
```
5. 编辑 `app` 的 `Configurations`, 在 `General` 的 `Before Launch` 插入刚创建的 `lejson` task, 放在 `Gradle-aware Make` 之前 
6. 每次 `run` 或 `debug` 会自动更新 模型代码 

**Windows系统请先安装 python2.7**


## 用法
```
usage: LeJson.py [-h] -d {mj,mt,yy,jo,gs,jc,fj,ls,le} [-o OUTPUT_PATH] [-f]
                 [-k] [--fp FIELD_PREFIX] [--cp CLASS_PREFIX] [--pkg PACKAGE]
                 [-b] [-s] [-e] [-t]
                 [input [input ...]]

自动生成JSON模型类

positional arguments:
  input                 json文件路径,如果是目录名,则处理目录下
                        所有一级.json文件;默认为当前路径

optional arguments:
  -h, --help            show this help message and exit
  -d {mj,mt,yy,jo,gs,jc,fj,ls,le}
                        采用的解析方法,必填.
  -o OUTPUT_PATH        输出路径,默认为当前路径
  -f                    强制更新,即使json未变化
                        ,也生成新的目标模型
  -k                    如果目标文件已经存在,则跳过
  --fp FIELD_PREFIX     生成字段的前缀
  --cp CLASS_PREFIX     输出结果类名的前缀
  --pkg PACKAGE         如果是Java类,需要指定其package;默认会根据
                        OUTPUT_PATH 计算
  -b                    生成Java代码的字段限定为public,不使用gett
                        er和setter
  -s                    不生成序列化代码,目前只用于 jo
  -e                    不生成反序列化代码,目前只用于 jo
  -t                    不生成string转换的方法,目前只用于 jo
```

## 目前支持以下8种解析Json方法
### Ojbective-C
1. mj [MJExtension](https://github.com/CoderMJLee/MJExtension)
2. mt [Mantle](https://github.com/Mantle/Mantle)
3. yy [YYModel](https://github.com/ibireme/YYModel)

### Java
1. jo [JSONObject](http://github.com/iwanglian/LeJson)
1. gs [gson](https://github.com/google/gson)
2. fj [fastjson](https://github.com/alibaba/fastjson)
3. jc [jackson](https://github.com/FasterXML/jackson)
4. ls [LoganSquare](https://github.com/bluelinelabs/LoganSquare)

## benchwork
在Sample工程中,记录了各个框架解析Json的耗时.
测试用例是 `知乎日报` 的最新消息, 有 200行数据, 详见  TestModel.json
运行1000次,在iPhone6s上时间分别为:

+ YYModel             0.127326
+ MJExtention         0.503630
+ Mantle              0.79556

在红米3上耗时为:

* JSONObject                       0.600000
* LoganSquare                      0.627000
* Gson                             0.649000
* Fastjson                         0.715000
* Jackson                          1.015000

平均到每次,都不会超过1ms ,执行速度不应该作为选择的主要因素.


## 为什么要做这个
以前一直使用`ProtoBuf` 作为数据序列化方案, 开发过程非常顺利.

ProtoBuf` 根据 `proto` 定义文件,使用工具自动生成 `Objective-C` 和 `Java` 代码, 再使用一些基础库,完成数据的 打包和解包.
开发同学只需要处理业务,而不用关心数据处理.

后来的项目, 更多的是使用Json , 在招聘iOS开发同学时, 多数都是在用 `Json` 作为App与Server通信的组织形式.

使用Json的最初级阶段,是将数据转化到一个 `NSDictionary` 里,然后通过字符串 `key` 来取值使用,
 不但需要手写解析逻辑, 工作量大, 容易拼错字符串, 而且对后台代码容错能力也很差.

第二阶段,是使用 `Mantle` 类的自动转型框架, 很大程度了解放了生产力, 项目中只需要定义好数据模型,就能自动转换得到.
这样,利用 `Objective-c` 的动态能力,反射出相应的请求类和响应类, 很快就写出一个 网络数据处理的 `Engine`.

第三阶段, 自动生成对象模型. Android开发很早就有了 [GsonFormat](https://github.com/zzz40500/GsonFormat) , 我仿照它实现了iOS版本,用在项目中.
结合第二阶段的工具, 简单的跑跑脚本,再改些配置, 就完成了一条网络协议的开发.

`LeJson` 是用 `Python` 写的,选择这个语言的理由,

1. 我比较熟悉, 之前也写了一些工具  [Tools](https://github.com/iwanglian/tools)
2. Mac系统自带, 不需要再安装软件.
3. 语法简单, 方便其它同事理解 ,并提出问题.
4. 命令执行,方便写入`Shell` 或 `batch` ,自动构建.

第一个版本写得很凌乱, 只支持 'Objective-c'中的 'MJExtention'  于是考虑重构, 诞生了这个第二版.


第二版将 `json` 解析成一个中间对象, 然后再根据不同语言的要求生成相应的代码. 
又参照 `GsonFormat` ,实现了 Java版本.

第三版是为了实现Java的兼容处理, 开发过程中重新整理了语法树模型.
有些创业公司的Server的程序使用了世界上最好的PHP语法开发, 输出的 `JSON` 非常灵活. 例如:
字段  `foo` 在语义上是 布尔型, 但PHP在 `true` 的时候输出字符串 `"1"` ,在 `false` 的时候输出数值 `0`. 
如果是使用iOS的 `YYModel` `MJExtention` 等库, 在 `Model` 里将 `foo` 字段类型定为 `BOOL`, 这些库会自动将灵活的值自动转型成相应的 `BOOL`值.

但是 Android 使用的几个模型库, 当类型不完全匹配时, 直接抛出异常, 不再往下解析下去了.显示 ,  `int`  `boolean`  `String` 都不能应对所有情况.
而原始的 `JSONObject` 由于不依赖模型里的类型,反而不会出错,并且提供了兼容处理的方法.

这里就提供 jo 解析方法, 先将内容转成 `JSONObject` , 再从中其值,放入模型中.
经过测试, jo 比其它方法,速度稍快, 且不依赖第三方库, 推荐使用
 



