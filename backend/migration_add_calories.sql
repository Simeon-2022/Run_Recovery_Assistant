-- Run this once in the Supabase SQL Editor (Dashboard → SQL Editor → New query)
-- Adds calories_per_100g column to the foods table.

ALTER TABLE foods
  ADD COLUMN IF NOT EXISTS calories_per_100g INTEGER NOT NULL DEFAULT 0;
