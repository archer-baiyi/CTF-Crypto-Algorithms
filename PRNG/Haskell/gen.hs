import System.Random (getStdGen, uniform, StdGen)
import Data.Word (Word64)
import Control.Monad (replicateM_)

printRandoms :: Int -> StdGen -> IO ()
printRandoms 0 _ = return ()
printRandoms n gen = do
    let (randNum, newGen) = uniform gen :: (Word64, StdGen)
    putStrLn $ show randNum
    printRandoms (n - 1) newGen

main :: IO ()
main = do
    gen <- getStdGen
    
    -- 连续生成5个随机数
    -- 前2个用于破解，后3个用于验证
    -- Generate 5 random numbers in a row
    -- Use the first 2 for cracking, and the last 3 for verification
    printRandoms 5 gen

-- 可以使用https://play.haskell.org/在线运行这段Haskell代码
-- You can run this Haskell code online at https://play.haskell.org/

-- 17586405056036639638
-- 4338398458645668384
-- 6633931353780533360
-- 1010696636966324438
-- 15964221105239425512