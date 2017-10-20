#coding=utf-8

imagePort_table = {
'46c2646d3ca51f2d2b92eb0dd52c272f' : '9797',
'eb4be6ba6a9909253530fb5b2f25a3cc' : '53218',
'04b04fddaced36f0e4817e6f23c0935d' : '3128',
'fc5b302987ea2ad0f32d0a47f7bcd18f' : '3128',
'f653d9951e57ffc112bcb8bb6abded75' : '80',
'b9d095697f4a15b7793e0ce36cc302e2' : '8081',
'61e9781fb5b64d0c697c02b1ff0542e8' : '9999',
'999385ceb64d3a9aef3bda75d764d0d4' : '80',
'76c747fa27d0800dbdcaf562b1dcb034' : '8080',
'20890428106e3176a52ba0f7c534e335' : '808',
'c0d3b315fde95dace662eface940dc0a':'26416',
'9b964d25d368ed1775fd37671b608d72':'8081',
'5991085ea439a68142470850e41bf91d':'8118',
'61eb52993a0cac3a63f697a0021932e4':'61234',
'7f157d550147cd33027afc2564ba77e3':'62225',
'e538ac755c4856670e0540bbda18063d':'8080',
'fd88c940bde8851cb54318bf29b3294f':'9000',
'e538ac755c4856670e0540bbda18063d':'8080',
'e652f80d7a2670833b3a85391563f852':'8123',
'0f5955a30f6210376f595e0b381ef627':'20717',
'29592736d86928a5403bd313fc2ff35c':'8118',
'59c5740e533bee03571e8a9c453526bd':'8888',
'cb1796d7b2b899456bf417d4c19531f1':'81',
'd974a0a6c3f054d452cb187c167d9fcc':'9999',
'59c5740e533bee03571e8a9c453526bd':'8888',
'46228de070f07be0432a5d3bef3bffc0':'84',
'6f43410163956ca01948ae994ce0beef':'808',
'b75e90980f3acf520fde02327110b976':'38308',
'e235c05fc0bc45b71690a3a4625af365':'8123'
};

def getImagePort(image):
    for name,value in imagePort_table.items():
        if name == image:
            return int(value);
    return None;
