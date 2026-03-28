import pdfplumber

pdf_files = [
    ('1774582650_52403_5c6c84f145ef24a507ab07fb1bd08ac6.pdf', 'PDF1'),
    ('1774582680_28943_01994e98b7e10e13a634d4538feed7f6.pdf', 'PDF2'),
    ('1774582890_61732_e26841673ec3b98cbcd6f06bb82bee3b.pdf', 'PDF3'),
    ('1774582890_95274_25401381.pdf', 'PDF4'),
    ('1774582890_96037_d222221b766d3855a47acd6a8cccde55.pdf', 'PDF5'),
    ('249008.pdf', 'PDF6'),
]

for pdf_file, label in pdf_files:
    try:
        with pdfplumber.open(pdf_file) as pdf:
            all_text = ''
            for page in pdf.pages[:5]:
                text = page.extract_text()
                if text:
                    all_text += text + '\n'
            
            print('\n' + '='*80)
            print(label + ': ' + pdf_file)
            print('Pages:', len(pdf.pages))
            print('\nContent (first 3000 chars):')
            print(all_text[:3000])
    except Exception as e:
        print('Error with ' + label + ': ' + str(e)[:100])
