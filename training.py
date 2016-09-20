import csv, png

with open('GZ_clean_abridged.csv') as inputfile:
	data = csv.DictReader(inputfile)
	with open('training_data_abridged.csv', 'w', newline='') as  outputfile:
		writer = csv.DictWriter(outputfile, ['OBJID', 'pixels', 'class'])
		writer.writeheader()
		
		for line in data:
			r = png.Reader("./images/" + line['OBJID'] + ".png")
			width, height, pixels, metadata = r.asRGB()

			i = 0
			luminance = [0.2126, 0.7152, 0.0722]
			lum_sum = 0
			img_lum = []

			
			for row in pixels:
				for p in row:
					lum_sum += p * luminance[i]
					i += 1
					if (i > 2):
						i = 0
						img_lum.append(lum_sum)
						lum_sum = 0

			max_lum = max(img_lum)
			img_lum = [str(l / max_lum) for l in img_lum]

			# stringify img_lum array and add to csv file
			c = '0'
			if (line['ELLIPTICAL'] == '1'):
				c = '1'
			if (line['UNCERTAIN'] == '1'):
				c = '2'

			pixels_string = ' '.join(img_lum)
			#print(pixels_string)
			row = {'OBJID': line['OBJID'], 'pixels': pixels_string, 'class': c}
			writer.writerow(row)
				


