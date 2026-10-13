-- Stores the administrator-selected theme shared by all site visitors.
CREATE TABLE IF NOT EXISTS platform_theme_settings (
    singleton_id SMALLINT PRIMARY KEY DEFAULT 1 CHECK (singleton_id = 1),
    theme TEXT NOT NULL DEFAULT 'light' CHECK (theme IN ('light', 'dark')),
    updated_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

INSERT INTO platform_theme_settings (singleton_id, theme)
VALUES (1, 'light')
ON CONFLICT (singleton_id) DO NOTHING;
