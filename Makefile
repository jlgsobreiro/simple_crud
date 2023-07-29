build: stop
	docker build --target crud -t crud .

start:
	docker compose up

stop:
	docker compose down

add_model:
	$(eval MODEL_NAME := $(shell bash -c 'read -p "Enter model name: " model_name; echo $$model_name'))
	echo Creating model file for $(MODEL_NAME)
	make create_model_file MODEL_NAME=$(MODEL_NAME)
	echo Creating repository file for $(MODEL_NAME)
	make create_repository_file MODEL_NAME=$(MODEL_NAME)
	echo Creating view file for $(MODEL_NAME)
	make create_view_file MODEL_NAME=$(MODEL_NAME)
	echo Creating registy on view setup for $(MODEL_NAME)
	make add_model_to_setup_view MODEL_NAME=$(MODEL_NAME)

create_model_file:
	cp -r ./models/ModelTemplate.py ./models/$(MODEL_NAME).py
	sed -i 's/ModelTemplate/$(MODEL_NAME)/g' ./src/models/$(MODEL_NAME).py

create_repository_file:
	cp -r ./repository/RepositoryTemplate.py ./repository/$(MODEL_NAME)Repository.py
	sed -i 's/ModelTemplateRepository/$(MODEL_NAME)Repository/g' ./src/repository/$(MODEL_NAME)Repository.py

create_view_file:
	cp -r ./view/ViewTemplate.py ./view/$(MODEL_NAME)View.py
	sed -i 's/ModelTemplateView/$(MODEL_NAME)View/g' ./src/view/$(MODEL_NAME)View.py

add_model_to_setup_view:
	sed -i 's/##Reserverd_for_import/##Reserverd_for_import\nfrom views.$(MODEL_NAME)View import $(MODEL_NAME)View\n/g' ./view/setup.py

	lowercaseview=$(echo $(MODEL_NAME)View | tr '[:upper:]' '[:lower:]')
	sed -i 's/##Reserverd_for_links_nav_bar/    ('$(lowercaseview)', '$(MODEL_NAME)'),\n##Reserverd_for_links_nav_bar\n/g' ./view/setup.py

	sed -i 's/##Reserverd_for_add_url_rule/    $(MODEL_NAME)View.add_url_rule(app)\n##Reserverd_for_add_url_rule\n/g' ./view/setup.py