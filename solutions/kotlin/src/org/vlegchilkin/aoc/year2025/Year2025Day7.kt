package org.vlegchilkin.aoc.year2025

import org.vlegchilkin.aoc.*


/**
 * 2025/7: Laboratories
 */
class Year2025Day7(input: String) : Solution {
  private val space = input.toCSpace()

  override fun partAB(): Pair<Int, Long> {
    var beamsByColumn = space.objects()['S']!!.map { it.second }.associateWith { 1L }
    var reflections = 0

    space.rows.drop(1).forEach { row ->
      val nextBeamsByColumn = mutableMapOf<Int, Long>()
      beamsByColumn.forEach { (col, beams) ->
        if ((row to col) !in space) {
          nextBeamsByColumn[col] = nextBeamsByColumn.getOrDefault(col, 0) + beams
        }
        else {
          reflections++
          if (col + 1 in space.cols) {
            nextBeamsByColumn[col + 1] = nextBeamsByColumn.getOrDefault(col + 1, 0) + beams
          }
          if (col - 1 in space.cols) {
            nextBeamsByColumn[col - 1] = nextBeamsByColumn.getOrDefault(col - 1, 0) + beams
          }
        }
      }
      beamsByColumn = nextBeamsByColumn
    }

    return reflections to beamsByColumn.values.sum()
  }
  companion object : Test(2025, 7, { Year2025Day7(it) })
}
