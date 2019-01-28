#coding=utf-8
#coding=GBK
#windows应用程序  
#使用类来描述  
from ctypes import *
from ctypes.wintypes import *
      
WS_EX_APPWINDOW = 0x40000
WS_OVERLAPPEDWINDOW = 0xcf0000
WS_CAPTION = 0xc00000
SW_SHOWNORMAL = 1
SW_SHOW = 5
CS_HREDRAW = 2
CS_VREDRAW = 1
CW_USEDEFAULT = 0x80000000
WM_DESTROY = 2
WHITE_BRUSH = 0
      
WNDPROCTYPE = WINFUNCTYPE(c_int, HWND, c_uint, WPARAM, LPARAM)  
#定义窗口类结构  
class WNDCLASSEX(Structure):  
    _fields_ = [("cbSize", c_uint),  
                ("style", c_uint),  
                ("lpfnWndProc", WNDPROCTYPE),  
                ("cbClsExtra", c_int),  
                ("cbWndExtra", c_int),  
                ("hInstance", HANDLE),  
                ("hIcon", HANDLE),  
                ("hCursor", HANDLE),  
                ("hBrush", HANDLE),  
                ("lpszMenuName", LPCWSTR),  
                ("lpszClassName", LPCWSTR),  
                ("hIconSm", HANDLE)]  
      
      
      
#开发人员：蔡军生（QQ：9073204） 深圳  2014-8-24  
#窗口类  
class Window:  
    def __init__(self, hWnd):  
        self.hWnd = hWnd  
    def Display(self, cmdShow):  
        windll.user32.ShowWindow(self.hWnd, cmdShow)  
        windll.user32.UpdateWindow(self.hWnd)  
         
#窗口类型注册类  
class WinClassMaker:  
    def __init__(self, wndProc, className, hInst):  
        self.wndClass = WNDCLASSEX()  
        self.wndClass.cbSize = sizeof(WNDCLASSEX)  
        self.wndClass.style = CS_HREDRAW | CS_VREDRAW  
        self.wndClass.lpfnWndProc = wndProc  
        self.wndClass.cbClsExtra = 0
        self.wndClass.cbWndExtra = 0
        self.wndClass.hInstance = hInst  
        self.wndClass.hIcon = 0
        self.wndClass.hCursor = 0
        self.wndClass.hBrush = windll.gdi32.GetStockObject(WHITE_BRUSH)  
        self.wndClass.lpszMenuName = 0
        self.wndClass.lpszClassName = className  
        self.wndClass.hIconSm = 0
    def Register(self):  
        return windll.user32.RegisterClassExW(byref(self.wndClass))  
      
#创建窗口  
class WinMaker:  
    def __init__(self, className, hInst):  
        self.className = className  
        self.hInst = hInst  
        self.style = WS_OVERLAPPEDWINDOW | WS_CAPTION  
        self.exStyle = 0
        self.x = CW_USEDEFAULT  
        self.y = 0
        self.width = CW_USEDEFAULT  
        self.height = 0
        self.hWndParent = HWND(0)  
        self.hMenu = HWND(0)  
        self.wndCreatData = c_void_p(0)  
    def Create(self, title):  
        self.hWnd = windll.user32.CreateWindowExW(  
            self.exStyle, self.className, title,  
            self.style,  
            self.x, self.y,  
            self.width, self.height,  
            self.hWndParent,  
            self.hMenu,   
            self.hInst,   
            self.wndCreatData)  
          
        if not self.hWnd:  
            print('Failed to create window')  
            exit(0)  
        return self.hWnd  
              
#窗口消息处理回调函数  
def PyWndProc(hWnd, Msg, wParam, lParam):  
    if Msg == WM_DESTROY:  
        windll.user32.PostQuitMessage(0)  
    else:  
        return windll.user32.DefWindowProcW(hWnd, Msg, wParam, lParam)  
    return 0
          
#主函数入口      
def main():   
    hInst = windll.kernel32.GetModuleHandleW(None)  
    WndProc = WNDPROCTYPE(PyWndProc)   
          
    className = u'ShenzhenCai'
    wname = u'Hello World' 
          
    winClass = WinClassMaker(WndProc, className, hInst)  
    winClass.Register()  
    maker = WinMaker(className, hInst)  
    win = Window(maker.Create(wname))  
    win.Display(SW_SHOW)  
          
    msg = MSG()  
    lpmsg = pointer(msg)  
    print('Entering message loop')  
    while windll.user32.GetMessageW(lpmsg, 0, 0, 0) != 0:  
        windll.user32.TranslateMessage(lpmsg)  
        windll.user32.DispatchMessageW(lpmsg)  
      
    print('done.')  
          
          
if __name__ == "__main__":  
    print( "Win32 Application in python" )  
    main()
    main()	
