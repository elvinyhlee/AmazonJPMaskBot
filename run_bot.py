from multiprocessing import Pool

from mask import MaskBot

targets = [
    ('B07573632C', 'fitty 60 普通size'),
    ('B01545GQ9O', 'fitty 30個 普通size 獨立包裝'),
    ('B01545GL76', 'fitty 30個 細size 獨立包裝'),
    ('B016DCAOOA', 'fitty 100個 普通size 獨立包裝'),
    ('B016DCAOZY', 'fitty 100個 細size 獨立包裝'),
    ('B016DCAOQI', 'fitty 100個 兒童size 獨立包裝'),
    ('B075MWTSMJ', 'fitty silky touch 50個 普通size'),
    ('B075MX4TB5', 'fitty silky touch 50個 細size'),

    ('B07MJKHYDC', '白元 30個*4盒 普通Size'),
    ('B0141ZPO1E', '白元 60個 普通Size'),
    ('B07RPN2Z9K', '白元 60個 細Size'),
    ('B07L96M287', '白元快適灰色 30個 普通Size'),
    ('B07ZPB2NQT', '白元快適防護 30*2個獨立包裝 普通'),

    ('B00YM1NSPC', '超立體 50個 普通Size'),

    ('B07571223K', 'BMC 80個獨立包裝 普通Size'),
    ('B0756ZZ9JQ', 'BMC 80個獨立包裝 細Size'),
    ('B008WX2OY2', 'BMC 50個 普通Size'),
    ('B00EP56O0G', 'BMC 60個 普通Size (要加骨）'),
    ('B07JBLS77Q', 'BMC 60個 無紡布 普通Size'),
    ('B075T6D8X5', 'BMC Medical 50個 普通Size'),

    # ('B07VBM91JB', '超快適 50個 日本製稍貴 普通Size'),

    ('B07ZPC6HV8', '快適 60個獨立包裝 細Size'),

    ('B07YV93GNH', 'SmartBasic 200個 稍大Size'),
    ('B07YV7YGXG', 'SmartBasic 200個 普通Size'),

    ('B00I7K9PW4', '醫療現場 60個 普通Size'),

    ('B000VQC0TW', 'Medicom safeMask defender'),
    ('B001LM46HY', 'Medicom safeMask'),

    ('B07T5V4TCV', 'Presto 200個 稍大Size'),
    ('B077ZC9D8R', 'Presto 120個 獨立包裝 稍大Size'),
    ('B07YY9T1FQ', 'Presto 120個 獨立包裝 普通Size'),

    ('B01613I79K', 'PIP 60個 普通Size（要加骨）'),

    ('B074KBQXNW', '快適 120個'),
    ('B074KB4DJ9', '快適 120個 細Size'),

    ('B07YXX7ZDN', 'Comdia 240個 普通Size'),
    ('B07YXX6SJF', 'Comdia 150個 普通Size'),
    ('B07YXXJWY4', 'Comdia 150枚 細Size'),

    ('B07BT44RM7', '原田産業 30個 女Size'),
    ('B015H3FYCI', '原田産業 50個 女Size'),
    ('B015H3G4OA', '原田産業 大人の贅沢マスク 50個'),
    ('B017W21ILI', '原田産業 大人の贅沢マスク 30個'),

    ('B003FGPHJU', '白十字 50個 普通Size'),
]


def run_bot(target_set):
    bot = MaskBot(target_set)
    bot.repeated_scan()


def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def run():
    p = Pool(5)
    p.map(run_bot, list(divide_chunks(targets, 8)))


if __name__ == '__main__':
    run()
