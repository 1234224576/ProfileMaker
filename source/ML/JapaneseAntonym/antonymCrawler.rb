require 'nokogiri'
require 'open-uri'

doc = Nokogiri::HTML.parse(open("http://hanntaigo.main.jp/"),nil,'UTF-8')

for ti in 2..28 do
	for tdi in 1..5 do
		for i in 1..30 do
			begin
				mainText = doc.xpath('//*[@id="content"]/table['+ti.to_s+']/tbody/tr/td['+tdi.to_s+']/text()['+i.to_s+']').text
				mainText = mainText.gsub("\n","").gsub(" ","").gsub("・","")
				if mainText != "" then
					texts = mainText.split("⇔")
					File.open("atonym.csv","a") do |file|
					  file.puts texts[0]+","+texts[1]
					end
				end
			rescue
				mainText = ""
			end
		end
	end
end

# //*[@id="content"]/table[2]/tbody/tr/td[2]/text()[1]
# //*[@id="content"]/table[3]/tbody/tr/td[1]/text()[1]
# //*[@id="content"]/table[10]/tbody/tr/td[1]/text()[1]

# tableが2から28
#tdが1から5
#語数が不明