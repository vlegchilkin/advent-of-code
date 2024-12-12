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
    garden.keys.asSequence().filter { pos -> pos !in regions }.forEach { pos ->
      regions[pos] = ++idCounter
      regions.fillByTemplate(pos, garden)
    }

    val regionPositions = regions.entries.groupBy({ it.value }, { it.key }).mapValues { it.value.toSet() }

    val regionPerimeter = regionPositions.mapValues { (_, positions) ->
      positions.sumOf { pos ->
        Direction.borders().count { (pos + it) !in positions }
      }
    }

    data class Corner(val side: Direction, val outer: Direction, val inner: Direction)

    val possibleCorners = listOf(Corner(N, W, NW), Corner(E, N, NE), Corner(S, E, SE), Corner(W, S, SW))

    val regionSides = regionPositions.mapValues { (_, positions) ->
      positions.sumOf { pos ->
        possibleCorners.count { (side, outer, inner) ->
          ((pos + side) !in positions) and (((pos + outer) !in positions) or ((pos + inner) in positions))
        }
      }
    }

    val partA = regionPositions.entries.sumOf { (id, region) -> region.size * regionPerimeter.getOrDefault(id, 0) }
    val partB = regionPositions.entries.sumOf { (id, region) -> region.size * regionSides.getOrDefault(id, 0) }
    return partA to partB
  }

  companion object : Test(2024, 12, { Year2024Day12(it) })
}
