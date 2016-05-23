//
//  ViewController.m
//  Sample
//
//  Created by alick on 5/18/16.
//  Copyright (c) 2016 lejson. All rights reserved.
//


#import "ViewController.h"
#import "MJExtension.h"
#import "NSObject+YYModel.h"
#import "MTLModel.h"
#import "MTLJSONAdapter.h"
#import "MJTestModel.h"
#import "YYTestModel.h"
#import "MTTestModel.h"


@interface ViewController ()

@end

@implementation ViewController


- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view, typically from a nib.
    NSString *filePath = [[NSBundle mainBundle] pathForResource:@"TestModel" ofType:@"json"];
    self.myData = [NSData dataWithContentsOfFile:filePath];


    @weakify(self)
    dispatch_async(dispatch_get_global_queue(0, 0), ^{

        int round = 1000;
        NSDate *beforeYY = [NSDate date];
        for (int i = 0; i < round; i++) {
            [self testYY];
        }
        NSDate *afterYY = [NSDate date];
        NSString *yyResult = [NSString stringWithFormat:@"YYModel(yy) run %d times, duration: %f\n", round, [afterYY timeIntervalSinceDate:beforeYY]];
        dispatch_async(dispatch_get_main_queue(), ^{
            @strongify(self)
            self.label.text = [NSString stringWithFormat:@"%@%@", self.label.text, yyResult];
        });

        NSDate *beforeMJ = [NSDate date];
        for (int i = 0; i < round; i++) {
            [self testMJ];
        }
        NSDate *afterMJ = [NSDate date];
        NSString *mjResult = [NSString stringWithFormat:@"MJExtension(mj) run %d times, duration: %f\n", round, [afterMJ timeIntervalSinceDate:beforeMJ]];
        dispatch_async(dispatch_get_main_queue(), ^{
            @strongify(self)
            self.label.text = [NSString stringWithFormat:@"%@%@", self.label.text, mjResult];
        });


        NSDate *beforeMT = [NSDate date];
        for (int i = 0; i < round; i++) {
            [self testMT];
        }
        NSDate *afterMT = [NSDate date];
        NSString *mtResult = [NSString stringWithFormat:@"Mantle(mt) run %dtimes, duration: %f\n", round, [afterMT timeIntervalSinceDate:beforeMT]];
        dispatch_async(dispatch_get_main_queue(), ^{
            @strongify(self)
            self.label.text = [NSString stringWithFormat:@"%@%@", self.label.text, mtResult];
        });


    });

    self.label = [[UILabel alloc] initWithFrame:CGRectMake(20, 40, self.view.bounds.size.width-40, 400)];
    self.label.textColor = [UIColor blackColor];
    self.label.font = [UIFont systemFontOfSize:16];
    self.label.numberOfLines = 0;
    self.label.text = @"begin run \n";

    [self.view addSubview:self.label];

}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

- (void)testMJ {
    MJTestModel *testModel = [MJTestModel mj_objectWithKeyValues:self.myData];
}

- (void)testYY {
    YYTestModel *testModel = [YYTestModel yy_modelWithJSON:self.myData];
}

- (void)testMT {
    NSDictionary *dict = [NSJSONSerialization JSONObjectWithData:self.myData options:nil error:nil];
    MTTestModel *testModel = [MTLJSONAdapter modelOfClass:[MTTestModel class] fromJSONDictionary:dict error:nil];
}


@end