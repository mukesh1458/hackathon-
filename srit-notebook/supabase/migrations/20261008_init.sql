-- Initial migration
CREATE TABLE users_profiles (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  username text NOT NULL,
  created_at timestamp with time zone DEFAULT now()
);
