package com.alibou.security.structure;

import com.alibou.security.exception.ResourceNotFoundException;
import com.alibou.security.law.entities.Law;
import com.alibou.security.structure.dto.StructureCreateDto;
import com.alibou.security.structure.dto.StructureResponseDto;
import com.alibou.security.structure.entity.Structure;
import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;
import org.springframework.web.servlet.support.ServletUriComponentsBuilder;

import java.util.List;
import java.util.Objects;
import java.util.UUID;

@Service
@RequiredArgsConstructor
@Transactional
public class StructureService {
    private final StructureRepository structureRepository;

    public Structure getStructureImage(String fileId) {
        return structureRepository
                .findById(UUID.fromString(fileId))
                .orElseThrow(() -> new ResourceNotFoundException("Could not find law with id - " + fileId));
    }


    public Structure getFile(String fileId) {
        return structureRepository
                .findById(UUID.fromString(fileId))
                .orElseThrow(() -> new ResourceNotFoundException("Could not find structure with id - " + fileId));
    }

    private String uriString(String id) {
        return ServletUriComponentsBuilder.fromCurrentContextPath()
                .path("/api/v1/public/structure/")
                .path(id)
                .toUriString();
    }

    public List<StructureResponseDto> getStructures() {
        List<Structure> structures = structureRepository.findAll();

        return structures.stream().map(structure -> {
            String uriString = uriString(structure.getId().toString());
            return new StructureResponseDto(
                    structure.getId(),
                    uriString
            );
        }).toList();
    }

    public void createStructure(StructureCreateDto structureCreateDto) throws Exception {
        try {
            String fileName = StringUtils.cleanPath(Objects.requireNonNull(structureCreateDto.getFile().getOriginalFilename()));

            if (fileName.contains("..") || fileName.isBlank()) {
                throw new Exception("Filename contains invalid path sequence " + fileName);
            }
            Structure structure = new Structure(
                    UUID.randomUUID(),
                    structureCreateDto.getFile().getBytes(),
                    structureCreateDto.getFile().getContentType(),
                    fileName
            );
            structureRepository.save(structure);
        } catch (Exception e) {
            throw new Exception("Could not save the file " + e);
        }
    }

    public void delete(UUID id) {
        structureRepository.findById(id).orElseThrow(() -> new ResourceNotFoundException("Could not find structure - " + id));
        structureRepository.deleteById(id);
    }
}
