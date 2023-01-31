using System;

namespace RandomNumberGenerator
{
    class Program
    {
        static void Main(string[] args)
        {
            Random random = new Random();
            while (true)
            {
                int number = random.Next(20, 23);
                Console.WriteLine(number);
            }
        }
    }
}
