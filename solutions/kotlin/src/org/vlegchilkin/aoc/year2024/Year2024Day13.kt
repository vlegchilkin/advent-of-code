package org.vlegchilkin.aoc.year2024

import org.vlegchilkin.aoc.*

typealias CL = List<Long>

/**
 * 2024/13: Claw Contraption
 */
class Year2024Day13(input: String) : Solution {
  private val games = input.toList("\n\n") { game ->
    val lines = game.split("\n").map { it.substringAfter(": ").toLongList() }
    Game(lines[0], lines[1], lines[2])
  }

  data class Game(val a: CL, val b: CL, val c: CL) {
    fun solve(): Pair<Long, Long>? {
      val top = c[0] * b[1] - c[1] * b[0]
      val bottom = b[1] * a[0] - a[1] * b[0]
      val x = (top / bottom).takeIf { top % bottom == 0L } ?: return null
      val y = (c[0] - a[0] * x) / b[0]
      return x to y
    }
  }

  override fun partA(): Any {
    val total = games.sumOf { game ->
      game.solve()?.let { 3 * it.first + it.second } ?: 0
    }
    return total
  }

  override fun partB(): Any {
    val total = games.map { game ->
      Game(game.a, game.b, game.c.map { it + 10000000000000 })
    }.sumOf { game ->
      game.solve()?.let { 3 * it.first + it.second } ?: 0
    }
    return total
  }

  companion object : Test(2024, 13, { Year2024Day13(it) })
}
