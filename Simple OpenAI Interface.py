import wx # wxPython
import sys, openai, os

prompt_list = [{"role": "system", "content": "Marline is a witty, dramatic, and gossipy informative chatbot."}]
model_name = 'YOUR TRAINED MODEL NAME' # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

def OpenAI_API():
    # Input your OpenAI Secret Key:
    os.environ['OPENAI_API_KEY'] = 'YOUR OPENAI SECRET KEY' # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    openai.api_key = os.getenv('OPENAI_API_KEY')

    # Connecting to the OpenAI API
    return openai.OpenAI()

class OpenAI_UI(wx.Frame):
	# wx.Frame must always be passed as the arguement for a class containing a Frame so that the class will inherit all the methods and attributes from Frame (this class is now a child class)
	## Frame = Window (but it is technically called a Frame in this case)
	# wxPython requires Frames to be in a class
	
	# constructor function 
	## These this initializing function will begin intializing when the class is called
	### In the case of a Frame, this will initialize when the application is starts
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, 'OpenAI Interface', size= (1000, 1000))

        panel = wx.Panel(self)

        st = wx.StaticText(panel, label= "Prompt:", pos= (75, 50))

        self.text_ctrl = wx.TextCtrl(panel, pos= (75, 75), size= (835, 50), style=wx.TE_MULTILINE|wx.TE_WORDWRAP)

        button = wx.Button(panel, label= 'Generate', pos= (75, 135), size= (835, 35))
        self.Bind(wx.EVT_BUTTON, self.generate, button)

        self.Show(True)

        self.log = wx.TextCtrl(panel, pos=(5, 175), size= (975, 775), style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_WORDWRAP)
        redir = RedirectText(self.log)
        sys.stdout = redir

    def generate(self, event):
        text = self.text_ctrl.GetValue() # Gets the text values within the text box
        if not text:
            print('No Text Inside the Box.')
        else:
            prompt_list.append({"role": "user", "content": text})
            client = OpenAI_API()
            print("Prompt:\n" + str(text))
            response = client.chat.completions.create(
                model=model_name,
                messages= prompt_list,
                temperature= 0.8
                )
            print("Response:\n" + response.choices[0].message.content + "\n")
            prompt_list.append({"role": "assistant", "content": response.choices[0].message.content})

        
class RedirectText(object): 
    '''
    Code copied from: https://stackoverflow.com/questions/54116987/how-to-embed-python-console-output-to-wxpython
    '''
    def __init__(self,aWxTextCtrl):
        self.out = aWxTextCtrl

    def write(self,string):
        self.out.WriteText(string)
		
		
if __name__ == '__main__':


	# Every wxPython application requires two things: a Application object and a Frame object
	# REQUIRED: This is the Application object, which basically runs the program
    app = wx.App()
	
    frame = OpenAI_UI(parent= None, id= wx.ID_ANY)
    app.MainLoop()