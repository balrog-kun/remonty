# -*- coding: utf-8 -*-

from roundup import password, date

#pri = db.getclass('priority')
#pri.create(name=''"critical", order="1")
#pri.create(name=''"urgent", order="2")
#pri.create(name=''"bug", order="3")
#pri.create(name=''"feature", order="4")
#pri.create(name=''"wish", order="5")

stat = db.getclass('status')
stat.create(name=''"nie-rozpoczety", order="1")
stat.create(name=''"w-trakcie", order="2")
stat.create(name=''"w-trakcie-opozniony", order="3")
stat.create(name=''"w-trakcie-do-poprawienia", order="4")
stat.create(name=''"zamkniety", order="5")
stat.create(name=''"zamkniety-do-poprawienia", order="6")
stat.create(name=''"brak-informacji", order="7")
stat.create(name=''"duplikat", order="8")

user = db.getclass('user')
user.create(osmid="anonymous", username="anonymous", roles='Anonymous')
#user.create(osmid="admin", username="admin", password=adminpw,
#    address='balrogg@gmail.com', roles='Admin')
#SHA: f8514ba7337f53b071f8b38d97699093b9867196
