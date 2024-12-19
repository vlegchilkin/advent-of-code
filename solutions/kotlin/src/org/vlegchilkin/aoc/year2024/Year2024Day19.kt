package org.vlegchilkin.aoc.year2024

import org.vlegchilkin.aoc.*


/**
 * 2024/19: Linen Layout
 */
class Year2024Day19(input: String) : Solution {
  private val towels: List<String>
  private val designs: List<String>

  init {
    val (towels, designs) = input.toList("\n\n") { it }
    this.towels = towels.split(", ")
    this.designs = designs.toList { it }
  }

  override fun partAB(): Pair<Int, Long> {
    fun numOfWays(design: String): Long {
      val lengthWays = mutableMapOf(0 to 1L)
      for (towelEnd in 1..design.length) {
        val possibleTowelStarts = towels.mapNotNull { towel ->
          val towelStart = towelEnd - towel.length
          lengthWays[towelStart]?.takeIf { design.substring(towelStart, towelEnd) == towel }
        }
        lengthWays[towelEnd] = possibleTowelStarts.sum()
      }
      return lengthWays.getValue(design.length)
    }

    val designWaysToBuild = designs.map { numOfWays(it) }
    val partA = designWaysToBuild.count { it > 0 }
    val partB = designWaysToBuild.sum()
    return partA to partB
  }

  companion object : Test(2024, 19, { Year2024Day19(it) })
}
