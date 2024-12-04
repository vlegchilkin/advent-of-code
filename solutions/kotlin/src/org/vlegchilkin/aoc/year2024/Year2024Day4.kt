package org.vlegchilkin.aoc.year2024

import org.vlegchilkin.aoc.*


/**
 * 2024/4: Ceres Search
 */
class Year2024Day4(input: String) : Solution {
  private val space = input.toCSpace { it }

  override fun partA(): Any {
    fun counter(pos: C): Int {
      val xmasDirections = "MAS".foldIndexed(Direction.all()) { index, validDirections, nextChar ->
        validDirections.filter { dir ->
          val nextPos = pos + dir.times(index + 1)
          space[nextPos] == nextChar
        }
      }
      return xmasDirections.size
    }

    val posCounter = space.filter { (_, c) -> c == 'X' }.map { (pos) -> pos to counter(pos) }
    val result = posCounter.sumOf { it.second }

    return result
  }

  override fun partB(): Any {
    val masWords = setOf("MAS", "SAM")
    val directions = listOf(Direction.NE, Direction.NW)

    val xmas = space.filter { (_, c) -> c == 'A' }.filter { (pos) ->
      val xWords = directions.map { dir -> "${space[pos + dir]}A${space[pos - dir]}" }
      xWords.count { it in masWords } == 2
    }

    return xmas.size
  }

  companion object : Test(2024, 4, { Year2024Day4(it) })
}
