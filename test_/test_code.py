import wearablevar as weav

data = weav.importe4('test_file.csv', '%m/%d/%Y %H:%M')

print('interdaysd is: ' + str(weav.interdaysd(data)))
print('interdaycv is: ' + str(weav.interdaycv(data)))
print('intradaysd is: ' + str(weav.intradaysd(data)))
print('intradaycv is: ' + str(weav.intradaycv(data)))
print('intradaymean is: ' + str(weav.intradaymean(data)))
print('TOR is: ' + str(weav.TOR(data)))
print('TIR is: ' + str(weav.TIR(data)))
print('POR is: ' + str(weav.POR(data)))
print('MASE is: ' + str(weav.MASE(data)))
print('summary is: ' + str(weav.summarymetrics(data)))

