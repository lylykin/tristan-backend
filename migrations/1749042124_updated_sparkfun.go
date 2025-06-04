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

		// add field
		if err := collection.Fields.AddMarshaledJSONAt(20, []byte(`{
			"cascadeDelete": false,
			"collectionId": "pbc_469820750",
			"hidden": false,
			"id": "relation3611712421",
			"maxSelect": 1,
			"minSelect": 0,
			"name": "borne",
			"presentable": false,
			"required": false,
			"system": false,
			"type": "relation"
		}`)); err != nil {
			return err
		}

		// add field
		if err := collection.Fields.AddMarshaledJSONAt(21, []byte(`{
			"cascadeDelete": false,
			"collectionId": "pbc_1279974871",
			"hidden": false,
			"id": "relation1187859512",
			"maxSelect": 1,
			"minSelect": 0,
			"name": "objet",
			"presentable": false,
			"required": false,
			"system": false,
			"type": "relation"
		}`)); err != nil {
			return err
		}

		return app.Save(collection)
	}, func(app core.App) error {
		collection, err := app.FindCollectionByNameOrId("pbc_4083066884")
		if err != nil {
			return err
		}

		// remove field
		collection.Fields.RemoveById("relation3611712421")

		// remove field
		collection.Fields.RemoveById("relation1187859512")

		return app.Save(collection)
	})
}
