import PySimpleGUI as sg
import compare
import json

sg.ChangeLookAndFeel('GreenTan')

layout = [
		[sg.Text('Import Profile', size=(15, 1), auto_size_text=False, justification='right'),      
	     sg.InputText(size=(85, 1)), sg.FileBrowse(), sg.Open()],
	    [sg.InputCombo([], size=(45, 10), key="selected_profile_1"), sg.Submit(key="submit_profile_1"),
	     sg.Text("Difference", size=(54,1), justification="center"),
	     sg.InputCombo([], size=(45, 10), key="selected_profile_2"), sg.Submit(key="submit_profile_2")],
	    [sg.Multiline(key="profile1", size=(55, 30)),
	     sg.Multiline(key="diff", size=(55, 30)),
	     sg.Multiline(key="profile2", size=(55, 30))],
	    [sg.Button("Compare"),sg.Quit()]  
	]
window = sg.Window('Slic3r profile comparer', default_element_size=(40, 1)).Layout(layout)

data = {}

while True:

	button, values = window.Read()

	if (button is "Quit") or (button is None) :
		break
	elif button is "Open":
		try:
			data = compare.process_config_file(values['Browse'], data)
			profile_options = compare.get_profile_list(data)
			window['selected_profile_1'].update(values=profile_options)
			window['selected_profile_2'].update(values=profile_options)
		except Exception as e:
			sg.Popup('Error opening file', e)

	elif button is "submit_profile_1":
		window['profile1'].update(json.dumps(data[values['selected_profile_1']], indent=2, sort_keys=True))
	elif button is "submit_profile_2":
		window['profile2'].update(json.dumps(data[values['selected_profile_2']], indent=2, sort_keys=True))
	elif button is "Compare":
		try:
			window["diff"].update(json.dumps(compare.return_config_diff(
				json.loads(values["profile1"]), json.loads(values["profile2"])),indent=2, sort_keys=True))
		except Exception as e:
			sg.Popup('Error comparing config, are they valid JSON values?', e)