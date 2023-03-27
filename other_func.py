def generate_image(main_data):
    lower, upper = 1, 15
    import os
    import re
    def find_fisker():
        fisker = []
        for i in list(dict(main_data["Art FAO"].value_counts()))[lower:upper]:
            try:

                fisker.append([f for f in os.listdir("fish") if re.search(i, f, flags=re.IGNORECASE)][0])
            except:
                
                pass
        return fisker

    counting_art = dict(main_data["Art FAO"].value_counts())
    values = [counting_art[i] for i in list(counting_art)[lower:upper]]
    tot_len = len(main_data)
    addresses = find_fisker()



    from PIL import Image
    import random
    from PIL import  Image, ImageDraw
    from PIL import ImageFont
    def create_bubble(percentage):
        image = Image.new('RGBA', (200, 200),color = (255, 255, 255, 0))
        draw = ImageDraw.Draw(image)
        draw.ellipse((0, 0, 200, 200), fill = 'white', outline ='white')
        font = ImageFont.truetype("Vogue.ttf", 120)
        draw.text((image.size[0]/2 - 50 , image.size[1]/2 -50),f"{str(percentage)} %",(0,0,0), font=font)
        return image 
    def create_bar(picture_width, add_this_text):
        image = Image.new('RGBA', (picture_width, 100),color = (255, 255, 255, 0))
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("Vogue.ttf", 100)
        draw.text((0 , image.size[1] -100),f"{add_this_text}",(0,0,0), font=font)
        return image 


    def is_overlap(l1, r1, l2, r2):
        if l1[0] > r2[0] or l2[0] > r1[0]:
            return False

        if l1[1] > r2[1] or l2[1] > r1[1]:
            return False

        return True


    background = Image.open('background.png').convert("RGBA")
    paste_image_list = [Image.open("fish/"+i).convert("RGBA") for i in addresses]

    font = ImageFont.truetype("Vogue.ttf", 100) 
    for i in range(len(paste_image_list)):
        paste_image_list[i].paste(create_bubble(int(100*values[i]/tot_len)), (int(paste_image_list[i].size[0]/2 -100),int(paste_image_list[i].size[1]/2-100)))
        #draw = ImageDraw.Draw(paste_image_list[i])
        #draw.text((paste_image_list[i].size[0]/2, paste_image_list[i].size[1]-100), "sample",(0,0,255),font=font)
        dectionary = {'taskekrabbe': 'marsupial crab', 'lyr': 'lyre', 'berggylt': 'ballan wrasse', 'sei': 'pollock', 'smørflyndre': 'righteye flounder', 'flekksteinbit': 'anarhichas minor', 'breiflabb': 'angler fish', 'dypvannsreke': 'deep water shrimp', 'rødspette': 'plaice', 'bergnebb': 'goldsinny wrasse', 'annen skate og rokke': 'other batoidea', 'sjøkreps': 'crayfish', 'brosme': 'cusk', 'kongekrabbe': 'king crab', 'gråsteinbit': 'atlantic wolffish', 'hyse': 'haddock', 'lange': 'common ling', 'lysing': 'european hake', 'sild': 'herring', 'grønngylt': 'corkwing wrasse', 'kveite': 'halibut', 'blåkveite': 'blue halibut', 'torsk': 'cod', 'makrell': 'mackerel'}	
        paste_image_list[i].paste(create_bar(paste_image_list[i].size[0], dectionary[addresses[i].replace(".png", "").lower().strip()]), (0,int(paste_image_list[i].size[1]-100)))



    for i in range(len(paste_image_list)):
        w = paste_image_list[i].size[0]
        h = paste_image_list[i].size[1]
        storrelse = w/h
        adjusted_w = int(storrelse*2000*(values[i]/tot_len))
        adjusted_h = int(2000*(values[i]/tot_len))


        paste_image_list[i]  = paste_image_list[i].resize((adjusted_w, adjusted_h))

    alread_paste_point_list = []

    for img in paste_image_list:
        # if all not overlap, find the none-overlap start point
        while True:
            # left-top point
            # x, y = random.randint(0, background.size[0]), random.randint(0, background.size[1])

            # if image need in the bg area, use this
            x, y = random.randint(0, max(0, background.size[0]-img.size[0])), random.randint(0, max(0, background.size[1]-img.size[1]))

            # right-bottom point
            l2, r2 = (x, y), (x+img.size[0], y+img.size[1])

            if all(not is_overlap(l1, r1, l2, r2) for l1, r1 in alread_paste_point_list):
                # save alreay pasted points for checking overlap
                alread_paste_point_list.append((l2, r2))
                background.paste(img, (x, y), img)
                break

    background.save("test.png")

    from itertools import combinations
    assert(all(not is_overlap(l1, r1, l2, r2) for (l1, r1), (l2, r2) in combinations(alread_paste_point_list, 2)))


