build: stop
	docker build --target crud -t crud .

start:
	docker compose up

stop:
	docker compose down

add_model:
	$(eval MODEL_NAME := $(shell bash -c 'read -p "Enter model name: " model_name; echo $$model_name'))
	@echo Creating model file for $(MODEL_NAME)
	@make create_model_file MODEL_NAME=$(MODEL_NAME)
	@echo Creating repository file for $(MODEL_NAME)
	@make create_repository_file MODEL_NAME=$(MODEL_NAME)
	@echo Creating view file for $(MODEL_NAME)
	@make create_view_file MODEL_NAME=$(MODEL_NAME)
	@echo Creating registy on view setup for $(MODEL_NAME)
	@make add_model_to_setup_view MODEL_NAME=$(MODEL_NAME)
	@echo Creating registy on forms for $(MODEL_NAME)
	@make add_model_to_forms MODEL_NAME=$(MODEL_NAME)

create_model_file:
	@cp -r ./models/ModelTemplate.py ./models/$(MODEL_NAME).py
	@sed -i 's/ModelTemplate/$(MODEL_NAME)/g' ./models/$(MODEL_NAME).py

create_repository_file:
	@cp -r ./repository/ModelTemplate.py ./repository/$(MODEL_NAME).py
	@sed -i 's/ModelTemplate/$(MODEL_NAME)/g' ./repository/$(MODEL_NAME).py

create_view_file:
	@cp -r ./views/ModelTemplate.py ./views/$(MODEL_NAME).py
	@sed -i 's/ModelTemplate/$(MODEL_NAME)/g' ./views/$(MODEL_NAME).py

add_model_to_setup_view:
	@sed -i 's/##Reserved_for_import/##Reserved_for_import\nfrom views.$(MODEL_NAME) import $(MODEL_NAME)View/g' ./views/setup.py

	@sed -i "s/##Reserved_for_links_nav_bar/    ('\/$$(echo $(MODEL_NAME)view | tr '[:upper:]' '[:lower:]')', '$(MODEL_NAME)'),\n##Reserved_for_links_nav_bar/g" ./views/setup.py

	@sed -i 's/##Reserved_for_add_url_rule/    $(MODEL_NAME)View.add_url_rule(app)\n##Reserved_for_add_url_rule/g' ./views/setup.py

add_model_to_forms:
	@sed -i 's/##Reserved_for_import/##Reserved_for_import\nfrom models.$(MODEL_NAME) import $(MODEL_NAME)/g' ./forms/Forms.py

	@sed -i 's/##Reserved_for_add_form_fields_by_model/\n\n@add_form_fields_by_model($(MODEL_NAME))\nclass $(MODEL_NAME)Form(FlaskForm):\n    def populated_obj(self):\n        return self.populate_obj($(MODEL_NAME))\n##Reserved_for_add_form_fields_by_model/g' ./forms/Forms.py

poetry_lock:
	docker exec simple_crud-simple_crud-1 poetry lock

poetry_install:
	docker exec simple_crud-simple_crud-1 poetry install

poetry_update:
	docker exec simple_crud-simple_crud-1 poetry update
