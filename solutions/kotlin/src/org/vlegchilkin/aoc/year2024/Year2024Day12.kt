package org.vlegchilkin.aoc.year2024

import org.vlegchilkin.aoc.*
import org.vlegchilkin.aoc.Direction.*


/**
 * 2024/12: Garden Groups
 */
class Year2024Day12(input: String) : Solution {
  private val garden = input.toCSpace { it }

  override fun partAB(): Pair<Int, Int> {
    val regions = CSpace<Int>(garden.rows, garden.cols, mutableMapOf())
    var idCounter = 0
    for ((pos) in garden) {
      if (pos in regions) continue
      regions[pos] = ++idCounter
      regions.fillByTemplate(pos, garden)
    }

    val areas = regions.values.groupBy { it }.mapValues { it.value.size }

    val perimeters = mutableMapOf<Int, Int>()
    for ((pos, id) in regions) {
      val cellPerimeter = Direction.borders().count { regions[pos + it] != id }
      perimeters[id] = perimeters.getOrDefault(id, 0) + cellPerimeter
    }

    data class Corner(val side: Direction, val outer: Direction, val inner: Direction)

    val possibleCorners = listOf(Corner(N, W, NW), Corner(E, N, NE), Corner(S, E, SE), Corner(W, S, SW))
    val sides = mutableMapOf<Int, Int>()
    for ((pos, id) in regions) {
      val corners = possibleCorners.sumOf { (side, outer, inner) ->
        val isCorner = (regions[pos + side] != id) and ((regions[pos + outer] != id) or (regions[pos + inner] == id))
        isCorner.toInt()
      }
      sides[id] = sides.getOrDefault(id, 0) + corners
    }


    val partA = areas.entries.sumOf { (id, area) -> area * perimeters.getOrDefault(id, 0) }
    val partB = areas.entries.sumOf { (id, area) -> area * sides.getOrDefault(id, 0) }
    return partA to partB
  }

  companion object : Test(2024, 12, { Year2024Day12(it) })
}
