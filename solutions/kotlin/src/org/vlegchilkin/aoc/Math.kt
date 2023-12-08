package org.vlegchilkin.aoc


/**
 * Least Common Multiple
 */
fun List<Int>.lcm(): Long {
  return this.fold(1L) { acc, c -> acc * c / gcd(acc, c.toLong()) }
}

/**
 * Least Common Multiple
 */
fun List<Long>.lcm(): Long {
  return this.fold(1L) { acc, c -> acc * c / gcd(acc, c) }
}

/**
 * Greatest Common Divisor
 */
tailrec fun gcd(a: Int, b: Int): Int = if (b == 0) a else gcd(b, a % b)

/**
 * Greatest Common Divisor
 */
tailrec fun gcd(a: Long, b: Long): Long = if (b == 0L) a else gcd(b, a % b)