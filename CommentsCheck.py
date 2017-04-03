from bs4 import BeautifulSoup
import sys
import os
import re

def comCheck(html_file):
	errors = {}
	comments = []
	soup = BeautifulSoup(open(html_file))
	for link in soup.find_all(class_="pad-tb5p"):
		try:
			bugId = link.get('id').encode("utf-8")
			print(bugId)
			comments.append(bugId + '\n')
			select = link.find('select', {'name': 'bugSelectStatus'})
			option = select.find('option', {'selected': 'selected'})
			bugStatus = option.get_text().replace("\n", " ").replace("\t", "").strip()
			print("Status" + "->" + bugStatus)
			comments.append("Status" + "->" + bugStatus + '\n')
			text = link.find('textarea', {'name': 'accountComments'})
			bugComments = text.get_text().encode("utf-8")
			if bugComments.strip() == "":
				errors[bugId] = "No comments"
				print("No comments" + '\n')
				comments.append("No comments" + '\n' * 2)
			else:
				tag = re.match('^\[.*(Exclude|Include|Flag)\]', bugComments.strip())
				if not tag:
					errors[bugId] = "No Tag, or tag is wrong"
				elif bugStatus.split()[0] != tag.group(1) and not (
						bugStatus.split()[0] == 'Flagged' and tag.group(1) == 'Flag'):
					errors[bugId] = "Tag and selected bug status not consistency"
				print(bugComments + '\n')
				comments.append(bugComments + '\n' * 2)
		except Exception, e:
			pass

	if len(errors):
		print("Notes: Total %d errors found like below:" % len(errors))
		for item in errors:
			if __name__ == "__main__":
				init(autoreset=True)
				print(Fore.RED + item + ":" + errors[item])
			else:
				sys.stdout.write(item + ":" + errors[item] + '\n', True)
	else:
		print("Congratuations, comments check okay")

	print('\n')

	try:
		file = os.path.join(os.getcwd(), '%s' % 'Component-' + soup.title.string.split()[3] + '.txt')
		fo = open(file, "w")
		fo.writelines(comments)
		fo.close()
		print("Save comments succeed!")
		print("Please find comments details on %s" % file)
	except Exception, e:
		print(str(e))
		print("\nSave comments to file failed!!!")


if __name__ == "__main__":
	from colorama import init, Fore
	comCheck(sys.argv[1])
