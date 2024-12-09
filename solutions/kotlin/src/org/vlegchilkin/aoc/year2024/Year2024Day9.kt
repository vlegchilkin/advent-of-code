package org.vlegchilkin.aoc.year2024

import org.vlegchilkin.aoc.*

const val EMPTY: Int = -1

data class File(val id: Int, val start: Int, val size: Int)

/**
 * 2024/9: Disk Fragmenter
 */
class Year2024Day9(input: String) : Solution {

  private val files: List<File>

  init {
    val clean = input.trim()
    val blocks = clean.padEnd(clean.length + 2 - (clean.length % 2), '0').map { it.digitToInt() }
    val files = mutableListOf<File>()
    blocks.chunked(2).foldIndexed(0) { fileId, offset, (fileSize, freeSpace) ->
      files += File(fileId, offset, fileSize)
      offset + fileSize + freeSpace
    }
    this.files = files
  }

  override fun partA(): Any {
    val diskSize = files.last().let { it.start + it.size }
    val disk = IntArray(diskSize) { EMPTY }

    this.files.forEach { file ->
      for (offset in file.start..<file.start + file.size) disk[offset] = file.id
    }

    var (lo, hi) = 0 to disk.indexOfLast { it != EMPTY }
    while (lo <= hi) {
      if (disk[lo] == EMPTY) {
        disk[lo] = disk[hi]
        disk[hi] = EMPTY
      }
      lo += 1
      while (disk[hi] == EMPTY) hi -= 1
    }

    val checksum = disk.mapIndexed { offset, fileId ->
      if (fileId != EMPTY) (offset * fileId).toLong() else 0L
    }.sum()
    return checksum
  }

  override fun partB(): Any {
    val files = this.files.toMutableList()  // todo rewrite based on linked lists with o(1) inserts

    files.reversed().forEach { fileToRelocate ->
      for (index in files.indices) {
        if (files[index].start >= fileToRelocate.start) break
        val freeSpace = files[index + 1].start - files[index].start - files[index].size
        if (freeSpace >= fileToRelocate.size) {
          files.add(index + 1, File(fileToRelocate.id, files[index].start + files[index].size, fileToRelocate.size))
          files.remove(fileToRelocate)
          break
        }
      }
    }

    val checksum = files.sumOf { file ->
      val offsets = IntRange(file.start, file.start + file.size - 1)
      offsets.sumOf { (file.id * it).toLong() }
    }
    return checksum
  }

  companion object : Test(2024, 9, { Year2024Day9(it) })
}
