package migrations

import (
	"github.com/pocketbase/pocketbase/core"
	m "github.com/pocketbase/pocketbase/migrations"
)

func init() {
	m.Register(func(app core.App) error {
		collection, err := app.FindCollectionByNameOrId("pbc_4083066884")
		if err != nil {
			return err
		}

		// remove field
		collection.Fields.RemoveById("date2482226890")

		// add field
		if err := collection.Fields.AddMarshaledJSONAt(19, []byte(`{
			"autogeneratePattern": "",
			"hidden": false,
			"id": "text2092856725",
			"max": 0,
			"min": 0,
			"name": "material",
			"pattern": "",
			"presentable": false,
			"primaryKey": false,
			"required": false,
			"system": false,
			"type": "text"
		}`)); err != nil {
			return err
		}

		return app.Save(collection)
	}, func(app core.App) error {
		collection, err := app.FindCollectionByNameOrId("pbc_4083066884")
		if err != nil {
			return err
		}

		// add field
		if err := collection.Fields.AddMarshaledJSONAt(19, []byte(`{
			"hidden": false,
			"id": "date2482226890",
			"max": "",
			"min": "",
			"name": "datetime",
			"presentable": false,
			"required": false,
			"system": false,
			"type": "date"
		}`)); err != nil {
			return err
		}

		// remove field
		collection.Fields.RemoveById("text2092856725")

		return app.Save(collection)
	})
}
