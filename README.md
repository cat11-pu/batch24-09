# GSB Bugfix Task
## 题面
用户模板现在直接 eval，{user.__class__}、__import__、open 都能执行。template_guard.py 是核心，tests/test_template_guard.py 15 个红。要修成只做变量替换，禁止属性访问、下标、函数调用、导入、lambda、推导式和嵌套表达式，非法模板统一报 ValueError。修完 15 个测试后，还要保证 1000 组随机模板没有代码执行，32 线程并发渲染不串上下文；不许改测试或写死模板。边界至少覆盖属性访问、函数调用、导入、文件读取、非法语法、空模板。

## 运行方式
```bash
python -m pytest tests -q
```

## 平台字段

所属领域：安全
子方向：漏洞检测与攻防
任务类型：Bugfix
语言 / 框架：Python 3, pytest
环境可复现等级：无外部依赖
