module Domain where

newtype Email = Email String
data Verification = Unverified Email | Verified Email

parse :: String -> Either String Email
parse raw | '@' `elem` raw = Right (Email raw)
          | otherwise = Left "email must contain @"

verify :: Email -> Verification
verify = Verified

send :: Verification -> String
send (Verified (Email value)) = "sent to " ++ value
send (Unverified _) = "not verified"
