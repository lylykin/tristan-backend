package migrations

import (
	"github.com/pocketbase/pocketbase/core"
	m "github.com/pocketbase/pocketbase/migrations"
)

func init() {
	m.Register(func(app core.App) error {
		collection, err := app.FindCollectionByNameOrId("pbc_1279974871")
		if err != nil {
			return err
		}

		// add field
		if err := collection.Fields.AddMarshaledJSONAt(2, []byte(`{
			"cascadeDelete": false,
			"collectionId": "pbc_1486587212",
			"hidden": false,
			"id": "relation416669013",
			"maxSelect": 1,
			"minSelect": 0,
			"name": "materiau",
			"presentable": false,
			"required": false,
			"system": false,
			"type": "relation"
		}`)); err != nil {
			return err
		}

		return app.Save(collection)
	}, func(app core.App) error {
		collection, err := app.FindCollectionByNameOrId("pbc_1279974871")
		if err != nil {
			return err
		}

		// remove field
		collection.Fields.RemoveById("relation416669013")

		return app.Save(collection)
	})
}
