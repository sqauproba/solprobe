// Package repositories abstracts persistence for the API.
package repositories

import (
	"context"
	"database/sql"
)

type SlotRepo struct {
	db *sql.DB
}

func NewSlotRepo(db *sql.DB) *SlotRepo {
	return &SlotRepo{db: db}
}

// Latest returns the most recently observed slot.
func (r *SlotRepo) Latest(ctx context.Context) (int64, error) {
	var slot int64
	err := r.db.QueryRowContext(ctx,
		"SELECT MAX(slot) FROM slots").Scan(&slot)
	if err == sql.ErrNoRows {
		return 0, nil
	}
	return slot, err
}

// InsertBatch writes a batch of slot events in a single transaction.
func (r *SlotRepo) InsertBatch(ctx context.Context, slots []Slot) error {
	tx, err := r.db.BeginTx(ctx, nil)
	if err != nil {
		return err
	}
	defer func() { _ = tx.Rollback() }()

	stmt, err := tx.PrepareContext(ctx,
		`INSERT INTO slots (slot, parent, root, status) VALUES ($1, $2, $3, $4)`)
	if err != nil {
		return err
	}
	defer stmt.Close()

	for _, s := range slots {
		if _, err := stmt.ExecContext(ctx, s.Slot, s.Parent, s.Root, s.Status); err != nil {
			return err
		}
	}
	return tx.Commit()
}

// Slot is a persisted slot event.
type Slot struct {
	Slot   int64
	Parent int64
	Root   int64
	Status string
}
