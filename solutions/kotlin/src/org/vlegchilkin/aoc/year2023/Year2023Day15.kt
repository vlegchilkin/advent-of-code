package org.vlegchilkin.aoc.year2023

import org.vlegchilkin.aoc.*


/**
 * 2023/15: Lens Library
 */
class Year2023Day15(input: String) : Solution {
  private val lines = input.toList(",") { it }
  private fun hash(s: String): Int {
    return s.fold(0) { acc, c -> (acc + c.code) * 17 % 256 }
  }

  override fun partA(): Any {
    return lines.sumOf { hash(it) }
  }

  override fun partB(): Any {
    val boxes = Array(256) { mutableMapOf<String, Int>() }
    for (line in lines) {
      if (line.endsWith('-')) {
        val label = line.removeSuffix("-")
        val box = boxes[hash(label)]
        box.remove(label)
      }
      else {
        val (label, focal) = line.split('=')
        val box = boxes[hash(label)]
        box[label] = focal.toInt()
      }
    }
    return boxes.mapIndexed { boxId, box ->
      box.values.mapIndexed { lensId, focal ->
        (boxId + 1) * (lensId + 1) * focal
      }.sum()
    }.sum()
  }

  companion object : Test(2023, 15, { Year2023Day15(it) })
}
