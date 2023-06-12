module Main where

flag = "Never_Gonna_Give_You_Up"

check_flag :: String -> Bool
check_flag input = input == ( "BtSCTF{" ++ flag ++ "}" )

main :: IO ()
main = do
  input <- getLine
  case check_flag input of
    True -> putStrLn "Correct Password :)"
    False -> putStrLn "Incorrect Password :("

