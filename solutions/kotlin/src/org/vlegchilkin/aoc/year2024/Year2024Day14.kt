package org.vlegchilkin.aoc.year2024

import org.vlegchilkin.aoc.*


data class Robot(val p: C, val v: C)

/**
 * 2024/14: Restroom Redoubt
 */
class Year2024Day14(input: String) : Solution {
  private val robots = input.toList { line -> line.toIntList().let { Robot(it[0] to it[1], it[2] to it[3]) } }
  private val n = 101
  private val m = 103

  private fun List<Robot>.emulate(seconds: Int): List<Robot> {
    return this.map { (p, v) ->
      val np = p + v * seconds
      Robot(p = np.mod(n to m), v = v)
    }
  }

  override fun partA(): Long {
    val robots = this.robots.emulate(100)

    val (nn, mm) = n / 2 to m / 2
    val quadrantCounter = robots
      .filter { (p) -> (p.first != nn) && (p.second != mm) }
      .map { (p) -> (p.first in 0 until nn) to (p.second in 0 until mm) }
      .groupBy { it }
      .mapValues { it.value.size }

    val safetyFactor = quadrantCounter.values.fold(1L, Long::times)
    return safetyFactor
  }

  override fun partB(): Int {
    fun view(robots: List<Robot>): String {
      val data = robots.map { (p) -> p.second to p.first }.associateWith { '*' }.toMutableMap()
      val space = CSpace(0..m, 0..n, data)
      return space.toString()
    }

    val patterns = listOf("*".repeat(10), "*.".repeat(10), "*..".repeat(10))
    for (seconds in 0..100_000_000) {
      val robots = this.robots.emulate(seconds)
      val picture = view(robots)

      if ( picture.findAnyOf(patterns) != null) {
        print(picture)
        return seconds
      }
    }
    error("Der Weihnachtsbaum is not found")
  }

  companion object : Test(2024, 14, { Year2024Day14(it) })
}
