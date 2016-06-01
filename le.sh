#!/bin/sh

objc_output="-o ios/Sample/Sample/Model"
objc_input='ios/Sample/Sample/Json'
prefix=''

python LeJson/lejson.py -d mj ${prefix} --cp MJ ${objc_output} ${objc_input}/TestModel.json -f
python LeJson/lejson.py -d yy ${prefix} --cp YY ${objc_output} ${objc_input}/TestModel.json -f
python LeJson/lejson.py -d mt ${prefix} --cp MT ${objc_output} ${objc_input}/TestModel.json -f

java_output="-o android/Sample/app/src/main/java/com/github/iwanglian/lejson/model"
java_package=""  #-k com.github.iwanglian.lejson.sample.model"
java_input="android/Sample/app/src/main/assets"
java_option="-f"

python LeJson/lejson.py -d gs ${prefix} --cp GS ${java_output}  ${java_package} ${java_input}/TestModel.json ${java_option}
python LeJson/lejson.py -d fj ${prefix} --cp FJ ${java_output}  ${java_package} ${java_input}/TestModel.json ${java_option}
python LeJson/lejson.py -d jc ${prefix} --cp JC ${java_output}  ${java_package} ${java_input}/TestModel.json ${java_option}
python LeJson/lejson.py -d ls ${prefix} --cp LS ${java_output}  ${java_package} ${java_input}/TestModel.json ${java_option}
python LeJson/lejson.py -d jo ${prefix} --cp JO ${java_output}  ${java_package} ${java_input}/TestModel.json ${java_option}
