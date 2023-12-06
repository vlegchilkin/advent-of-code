package org.vlegchilkin.aoc.year2023

import org.vlegchilkin.aoc.*


/**
 * 2023/6: Wait For It
 */
class Year2023Day6(input: String) : Solution {
  private val games: List<Pair<Long, Long>>

  init {
    val (time, distance) = input.toList { it.toLongList() }
    games = time.zip(distance)
  }

  override fun partAB(): Pair<Any, Any> {
    fun calc(games: List<Pair<Long, Long>>): Long {
      return games.fold(1L) { acc, (time, distance) ->
        acc * (1..time).count { it * (time - it) > distance }
      }
    }

    val single = games.fold("" to "") { acc, c -> acc.first + c.first to acc.second + c.second }.toLong()
    return calc(games) to calc(listOf(single))
  }

  companion object : Test(2023, 6, { Year2023Day6(it) })
}
