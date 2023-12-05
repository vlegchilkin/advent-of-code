package org.vlegchilkin.aoc.year2023

import org.vlegchilkin.aoc.Solution
import org.vlegchilkin.aoc.Test
import org.vlegchilkin.aoc.toList


/**
 * 2023/2: Cube Conundrum
 */
class Year2023Day2(input: String) : Solution {
  private val games = input.toList { game ->
    val regex = """^Game (\d+): (.*)$""".toRegex()
    val (id, details) = regex.matchEntire(game)!!.destructured
    id.toInt() to details.split("; ").map { set ->
      set.split(", ").associate { cube ->
        val (a, b) = cube.split(" ")
        b to a.toInt()
      }
    }
  }.toMap()

  override fun partA(): Any {
    val limits = mapOf("red" to 12, "green" to 13, "blue" to 14)
    return games.filter { (_, sets) ->
      sets.all { it.all { (color, count) -> limits[color]!! >= count } }
    }.keys.sum()
  }

  override fun partB(): Any {
    fun powerOfMin(sets: List<Map<String, Int>>): Int {
      val best = mutableMapOf<String, Int>()
      sets.forEach { set ->
        set.forEach { (color, count) ->
          best.compute(color) { _, old -> maxOf((old ?: 0), count) }
        }
      }
      return best.values.reduce { a, b -> a * b }
    }
    return games.values.sumOf { powerOfMin(it) }
  }

  companion object : Test(2023, 2, { Year2023Day2(it) })
}